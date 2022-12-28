import data_crud
import db
import xml_generator
import csv_generator
import json_generator
import xml_import
import csv_import
import json_import
import logging

module_logger = logging.getLogger("phonebookApp.controller")

def open_db():
    db.create_my_phonebook()

# запрос всех записей из базы
def all_rows():
    new_conn = db.create_connection()
    rows = data_crud.select_all(new_conn)
    db.close_connection(new_conn)
    dataset = [d for d in rows]
    return dataset

# поиск записей по условию
def find_rows(find_field,find_str):
    new_conn = db.create_connection()
    find_rows = data_crud.select_param(new_conn,find_field,find_str)
    db.close_connection(new_conn)
    dataset = [d for d in find_rows]
    logger = logging.getLogger("phonebookApp.controller.find")
    logger.info("finded {} records".format(len(dataset)))
    return dataset

# дублирование записи
def duplicat_row(id):
    new_conn = db.create_connection()
    new_row = data_crud.select_rowid(new_conn, id)
    new_data = (new_row[1], new_row[2], new_row[3], new_row[4])
    data_crud.insert_row(new_conn,new_data)
    db.close_connection(new_conn)

# обновление записи
def update_row(data):
    new_conn = db.create_connection()
    data_crud.update_row(new_conn,data)
    db.close_connection(new_conn)

# добавление записи
def insert_row(data):
    new_conn = db.create_connection()
    id = data_crud.insert_row(new_conn, data)
    logger = logging.getLogger("phonebookApp.controller.insert")
    logger.info("Isert data {} with id = {} ".format(data, id))
    db.close_connection(new_conn)

# удаление записи
def delete_row(id):
    new_conn = db.create_connection()
    data_crud.delete_row(new_conn, id)
    db.close_connection(new_conn) 

# удаление всех записей
def delete_all():
    new_conn = db.create_connection()
    data_crud.clear_all(new_conn)
    db.close_connection(new_conn) 

# выгрузка в xml, csv, json
def export_data(type_file):
    dataset = all_rows()
    match type_file:
        case "xml":
            xml_generator.create(dataset)
        case "csv":
            csv_generator.create(dataset)
        case "json":
            json_generator.create(dataset)

# импорт xml
def import_xml(f_path):
    if xml_import.parseXML(f_path):
        datalist= xml_import.arrayXML(f_path)
        if not datalist:
            message = "No data"
        else:
            try:
                import_data(datalist)
                message = "Success"
            except Exception as e:
                message = "Error insert to DB"
    else:
        message = "Bad structure"
    return message

# импорт csv
def import_csv(f_path):
    datalist = csv_import.parseCSV(f_path)
    if not datalist:
        message = "No data"
    elif datalist[0]== 'Bad structure':
        message = datalist[0]
    else:
        try:
            import_data(datalist)
            message = "Success"
        except Exception as e:
            message = "Error insert to DB"
    return message

# импорт json
def import_json(f_path):
    if json_import.parseJS(f_path):
        datalist = json_import.importJS(f_path)
        if not datalist:
            message = "No data"
        else:
            try:
                import_data(datalist)
                message = "Success"
            except Exception as e:
                message = "Error insert to DB"
    else:
        message = "Bad structure"
    return message

# запись в БД набора строк из массива
def import_data(datalist:list):
    for d in datalist:
        insert_row(d)
    logger = logging.getLogger("phonebookApp.controller.import")
    logger.info("Imported {} records".format(len(datalist)))
   



