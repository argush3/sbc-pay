"""notification tables added

Revision ID: 8f550bdc9491
Revises: 71c733c91cbf
Create Date: 2020-08-25 22:20:20.192383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f550bdc9491'
down_revision = '71c733c91cbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    notification_status_code_table = op.create_table('notification_status_code',
    sa.Column('code', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('code')
    )
    op.bulk_insert(
        notification_status_code_table,
        [
            {'code': 'PENDING', 'description': 'Mail Pending'},
            {'code': 'PROCESSING', 'description': 'Mail Processing'},
            {'code': 'SUCCESS', 'description': 'Mail Sent Successfully'},
            {'code': 'SKIP', 'description': 'No mail needed'},
            {'code': 'FAILED', 'description': 'Mail failed'},
        ]
    )


    op.create_table('statement_recipients',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('auth_user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=200), nullable=True),
    sa.Column('last_name', sa.String(length=200), nullable=True),
    sa.Column('email', sa.String(length=200), nullable=True),
    sa.Column('payment_account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['payment_account_id'], ['payment_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_statement_recipients_auth_user_id'), 'statement_recipients', ['auth_user_id'], unique=False)
    op.create_index(op.f('ix_statement_recipients_payment_account_id'), 'statement_recipients', ['payment_account_id'], unique=False)
    op.add_column('payment_account', sa.Column('auth_account_name', sa.String(length=250), nullable=True))
    op.add_column('payment_account', sa.Column('statement_notification_enabled', sa.Boolean(), nullable=True))
    op.execute("update payment_account set statement_notification_enabled='False'")
    op.add_column('statement', sa.Column('notification_date', sa.Date(), nullable=True))
    op.add_column('statement', sa.Column('notification_status_code', sa.String(length=20), nullable=True))
    op.create_foreign_key('statement_notification_status_code_Fk', 'statement', 'notification_status_code', ['notification_status_code'], ['code'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('statement_notification_status_code_Fk', 'statement', type_='foreignkey')
    op.drop_column('statement', 'notification_status_code')
    op.drop_column('statement', 'notification_date')
    op.drop_column('payment_account', 'statement_notification_enabled')
    op.drop_column('payment_account', 'auth_account_name')
    op.drop_index(op.f('ix_statement_recipients_payment_account_id'), table_name='statement_recipients')
    op.drop_index(op.f('ix_statement_recipients_auth_user_id'), table_name='statement_recipients')
    op.drop_table('statement_recipients')
    op.drop_table('notification_status_code')
    # ### end Alembic commands ###
