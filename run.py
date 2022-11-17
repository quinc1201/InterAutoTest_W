import os
import pytest
from config import conf


if __name__ == '__main__':
    report_path = conf.get_report_path() + os.sep + 'result'
    report_html_path = conf.get_report_path() + os.sep + 'html'
    pytest.main(['-vs', '--alluredir', report_path])