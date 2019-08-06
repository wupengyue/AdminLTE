""" 
@author:
@file: urls.py 
@time: 2018/1/31 13:20 
"""
from app.case.views import *
from app.case import case

case.add_url_rule('/add_cases', view_func=AddtestcaseView.as_view('add_cases'))
case.add_url_rule('/edit_case/<int:id>', view_func=EditcaseView.as_view('edit_case'))
case.add_url_rule('/import_cases', view_func=DaorucaseView.as_view('import_cases'))
case.add_url_rule('/ser_yongli', view_func=SeryongliView.as_view('ser_yongli'))
case.add_url_rule('/makeonlyonecase', view_func=MakeonlyoneCase.as_view('makeonlyonecase'))
case.add_url_rule('/duoyongli', view_func=DuoyongliView.as_view('duoyongli'))
case.add_url_rule('/export_cases', view_func=ExportCase.as_view('export_cases'))
case.add_url_rule('/caseonedeteil', view_func=OnecaseDetial.as_view('caseonedeteil'))
