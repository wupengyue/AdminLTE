# 管理后台
from app import admin
from app.models import db, Task, Interface, InterfaceTest, MockServer, User
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):

    column_labels = dict(
        username=u'用户名',
        user_email=u'用户邮件',
        status=u'状态',
        is_sper=u'权限',
        titles=u'职位',
        password=u'密码'
    )


admin.add_view(UserAdmin(User, db.session, name=u'用户', endpoint='adminuser'))
admin.add_view(ModelView(Task, db.session, name='定时任务', endpoint='tingtask'))
admin.add_view(ModelView(InterfaceTest, db.session, name='测试用例', endpoint='testcase'))
admin.add_view(ModelView(Interface, db.session, name='接口', endpoint='jiekou'))
admin.add_view(ModelView(MockServer, db.session, name='mock'))

