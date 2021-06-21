import os

from jobbole.qcc.cookie import MysqlConnector
from jobbole import settings
from jobbole.utils.excel_handler import ExcelHandler


def batch_update_company_info(filename):
    '''
    批量更新qcc的其他字段信息
    :return:
    '''

    cursor = MysqlConnector().cursor

    # 需要更新的企业名称
    update_company_list = []
    query_update_company = '''
        select name from qcc_company where get_money is null
        '''

    cursor.execute(query_update_company)
    company_names_tuple = cursor.fetchall()
    for company_name_tuple in company_names_tuple:
        company_name = company_name_tuple[0]
        update_company_list.append(company_name)

    print(len(update_company_list))

    update_company_sql = '''
       update qcc_company set get_money=%s,contact_phone=%s,payment_people=%s 
       where name=%s
       '''

    update_company_data = []

    excel_handler = ExcelHandler(os.path.join(settings.COMPANY_EXCEL_PATH_DIR,filename))
    nrows = excel_handler.nrows()
    for row_num in range(1,nrows):
        company_info = excel_handler.get_row_values(row_num)
        if company_info[0] in update_company_list:
            update_arg = (
                company_info[3], # get money
                company_info[5],  # contact_phone
                company_info[2],  # payment_people
                company_info[0] # company nmae
            )
            update_company_data.append(update_arg)

    print(len(update_company_data))
    cursor.executemany(update_company_sql,update_company_data)

if __name__ == '__main__':
    batch_update_company_info('companys.xlsx')