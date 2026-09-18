import os
os.environ['DATABASE_URL'] = 'sqlite://'
import unittest
from decimal import Decimal
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from banking.main import app
from banking.database import Base, get_db
from banking.models import User, Deposit, Transaction
from banking.core.security import hash_password

class BankingTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
        event.listen(self.engine, 'connect', lambda connection, _: connection.execute('PRAGMA foreign_keys=ON'))
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(self.engine, expire_on_commit=False)
        def database():
            with self.sessions() as db:
                try:
                    yield db
                except Exception:
                    db.rollback()
                    raise
        app.dependency_overrides[get_db] = database
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.engine.dispose()

    def user(self, name='alice', balance='100.00'):
        response = self.client.post('/users/', json=dict(nickname=name, first_name='First', last_name='Last',
            email=f'{name}@example.com', phone_number='1234567' if name=='alice' else '7654321',
            password='password!', balance=balance))
        self.assertEqual(response.status_code, 201, response.text)
        self.assertNotIn('password', response.json())
        return response.json()['id']

    def test_user_lifecycle_and_legacy_hash(self):
        uid = self.user()
        with self.sessions() as db:
            self.assertEqual(db.get(User, uid).password, hash_password('password!'))
        self.assertEqual(self.client.get('/users/?nickname=alice').json()[0]['id'], uid)
        self.assertNotIn('password', self.client.get('/users/').json()[0])
        self.assertEqual(self.client.patch(f'/users/{uid}', json={'nickname':'new', 'password':'changed!'}).status_code,200)
        with self.sessions() as db:
            self.assertEqual(db.get(User, uid).password, hash_password('changed!'))
        self.assertEqual(self.client.delete(f'/users/{uid}').status_code,204)
        self.assertEqual(self.client.get(f'/users/{uid}').status_code,404)

    def test_deposit_transfer_history_and_protected_delete(self):
        a,b=self.user(),self.user('bob','0')
        self.assertEqual(self.client.post('/deposits/',json={'user_id':a,'amount':'0.15'}).status_code,201)
        self.assertEqual(self.client.post('/transactions/',json={'sender_id':a,'recipient_id':b,'amount':'20.10'}).status_code,201)
        self.assertEqual(Decimal(self.client.get(f'/users/{a}').json()['balance']),Decimal('80.05'))
        self.assertEqual(Decimal(self.client.get(f'/users/{b}').json()['balance']),Decimal('20.10'))
        self.assertEqual(len(self.client.get(f'/transactions/user/{b}').json()),1)
        self.assertEqual(self.client.delete(f'/users/{a}').status_code,409)
        self.assertEqual(self.client.get('/deposits/1').status_code,200)
        self.assertEqual(self.client.get('/transactions/1').status_code,200)

    def test_invalid_transfer_leaves_balances_unchanged(self):
        a,b=self.user(),self.user('bob','0')
        for sender,recipient,amount,status in [(a,b,'101',409),(a,a,'1',400),(a,999,'1',404),(a,b,'-1',422),(a,b,'0.001',422)]:
            self.assertEqual(self.client.post('/transactions/',json={'sender_id':sender,'recipient_id':recipient,'amount':amount}).status_code,status)
        self.assertEqual(self.client.get('/transactions/').json(),[])
        self.assertEqual(Decimal(self.client.get(f'/users/{a}').json()['balance']),Decimal('100'))

    def test_validation_and_conflicts(self):
        a,b=self.user(),self.user('bob')
        self.assertEqual(self.client.patch(f'/users/{b}',json={'nickname':'alice'}).status_code,409)
        self.assertEqual(self.client.get(f'/users/{b}').json()['nickname'],'bob')
        for data in [{'nickname':None},{},{'balance':0},{'password':'weakpass'},{'phone_number':'letters'}]:
            self.assertEqual(self.client.patch(f'/users/{a}',json=data).status_code,422)
        for amount in ['0','-1','NaN','Infinity','0.001','100000000']:
            self.assertEqual(self.client.post('/deposits/',json={'user_id':a,'amount':amount}).status_code,422)
        self.assertEqual(self.client.post('/deposits/',json={'user_id':999,'amount':'1'}).status_code,404)

    def test_capacity_and_rollback_on_insert_failure(self):
        a,b=self.user(balance='99999999.99'),self.user('bob','10')
        self.assertEqual(self.client.post('/deposits/',json={'user_id':a,'amount':'0.01'}).status_code,409)
        self.assertEqual(self.client.post('/transactions/',json={'sender_id':b,'recipient_id':a,'amount':'1'}).status_code,409)
        from sqlalchemy.exc import SQLAlchemyError
        from sqlalchemy.orm import Session
        with patch.object(Session,'flush',side_effect=SQLAlchemyError('simulated failure')):
            self.assertEqual(self.client.post('/deposits/',json={'user_id':b,'amount':'1'}).status_code,503)
        with self.sessions() as db:
            self.assertEqual(db.get(User,b).balance,Decimal('10'))
            self.assertEqual(db.scalar(select(func.count()).select_from(Deposit)),0)

if __name__=='__main__':
    unittest.main()
