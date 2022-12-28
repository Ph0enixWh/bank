import tkinter as tk
from tkinter import ttk
import psycopg2
from config import host1, user1, password1, db_name1
import hashlib
import datetime

connection = psycopg2.connect(host=host1, user=user1, password=password1, database=db_name1)
cursor = connection.cursor()
connection.autocommit = True

def select_radiobutton():
    if select.get() == 0:
        label_auth.config(text='Почта')
    if select.get() == 1:
        label_auth.config(text='Логин')

#Окно регистрации
def btn_reg_click():
    global win_reg 
    win_reg = tk.Toplevel()
    win_reg.protocol("WM_DELETE_WINDOW", on_closing_reg)
    win_reg.geometry('500x500+100+100')
    win_entry.withdraw()

    tk.Label(win_reg, text= 'Имя', font=('Calibri', 14), pady=5).grid(
        row=0, column=0, sticky='we')
    tk.Label(win_reg, text= 'Отчество', font=('Calibri', 14), pady=5).grid(
        row=1, column=0, sticky='we')
    tk.Label(win_reg, text= 'Фамилия', font=('Calibri', 14), pady=5).grid(
        row=2, column=0, sticky='we')
    tk.Label(win_reg, text= 'Номер телефона', font=('Calibri', 14), pady=5).grid(
        row=3, column=0, sticky='we')
    tk.Label(win_reg, text= 'Почта', font=('Calibri', 14), pady=5).grid(
        row=4, column=0, sticky='we')
    tk.Label(win_reg, text= 'Адрес', font=('Calibri', 14), pady=5).grid(
        row=5, column=0, sticky='we')
    tk.Label(win_reg, text= 'Образование', font=('Calibri', 14), pady=5).grid(
        row=6, column=0, sticky='we')
    tk.Label(win_reg, text= 'Пароль', font=('Calibri', 14), pady=5).grid(
        row=7, column=0, sticky='we')

    tk.Button(win_reg, text='Регистрация', font=('Calibri', 12), command=btn_reg_click2).grid(
        row=8, column=1, sticky='e')
    
    global entry_name, entry_middle, entry_surname, entry_phone, entry_email, entry_address, entry_education, entry_password2

    entry_name = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_middle = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_surname = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_phone = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_email = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_address = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_education = tk.Entry(win_reg, font=('Calibri', 14), width=20)
    entry_password2 = tk.Entry(win_reg, font=('Calibri', 14), width=20, show='*')

    entry_name.grid(row=0, column=1)
    entry_middle.grid(row=1, column=1)
    entry_surname.grid(row=2, column=1)
    entry_phone.grid(row=3, column=1)
    entry_email.grid(row=4, column=1)
    entry_address.grid(row=5, column=1)
    entry_education.grid(row=6, column=1)
    entry_password2.grid(row=7, column=1)

#Вносим данные нового пользователя в таблицу
def btn_reg_click2():
    if (entry_password2.get() != ''):
        ps = entry_password2.get()
        hash = hashlib.md5(ps.encode())
        hash_ps = hash.hexdigest()

    if (entry_name.get() != '' and entry_middle.get() != '' and
        entry_surname.get() != '' and entry_phone.get() != '' and 
        entry_email.get() != '' and entry_address. get() != '' and 
        entry_education.get() != '' and hash_ps != ''):

        cursor.execute(
            f"""call reg('{entry_surname.get()} {entry_name.get()} {entry_middle.get()}', '{entry_phone.get()}', 
            '{entry_email.get()}', '{entry_address.get()}', '{entry_education.get()}', '{hash_ps}');"""
        )

def on_closing_reg():
    win_entry.deiconify()
    win_reg.destroy()

#Вход
def btn_entry_click ():
    global Name
    ps = entry_password.get()
    hash = hashlib.md5(ps.encode())
    hash_ps = hash.hexdigest()

    if select.get() == 0:
        cursor.execute(
            f"""select enter('{entry_login.get()}', '{hash_ps}')"""
        )
        Name = cursor.fetchall()

        if  str(Name[0]).strip('(,)') != 'None':
            global email
            email = entry_login.get()
            cursor.execute("""set role client""")
            client()
    else:
        cursor.execute(
            f"""select enter_empl('{entry_login.get()}', '{hash_ps}')"""
        )
        Name = cursor.fetchall()

        if  str(Name[0]).strip('(,)') != 'None':
            cursor.execute(f"""set role {entry_login.get()}""")
            employee()

#Окно клиента 
def client():
    global win_client, N
    win_client = tk.Toplevel()
    win_client.protocol("WM_DELETE_WINDOW", on_closing_client)
    win_client.geometry('500x500+100+100')
    win_entry.withdraw()

    N = str(Name[0]).strip("(,)'")
    cursor.execute(f"""select get_accounts('{N}', '{email}')""")
    list = cursor.fetchall()
    l = str(list[0]).split(",")
    rub = l[0].strip("(,)'")
    usd = l[1].strip("(,)'")
    eur = l[2].strip("(,)'")
    usd_b = l[3].strip("(,)'")
    eur_b = l[4].strip("(,)'")

    label_name = tk.Label(win_client, text=N.split()[1:], font=('Calibri', 14), pady=5)
    label_rub = tk.Label(win_client, text=round(float(rub), 2), font=('Calibri', 14), pady=5)
    label_usd = tk.Label(win_client, text=round(float(usd), 2), font=('Calibri', 14), pady=5)
    label_eur = tk.Label(win_client, text=round(float(eur), 2), font=('Calibri', 14), pady=5)
    label_usd_b = tk.Label(win_client, text=round(float(usd_b), 2), font=('Calibri', 14), pady=5)
    label_eur_b = tk.Label(win_client, text=round(float(eur_b), 2), font=('Calibri', 14), pady=5)

    tk.Label(win_client, text='Цена покупки', font=('Calibri', 12)).grid(
        row=1, column=2)
    tk.Label(win_client, text='rub', font=('Calibri', 14)).grid(
        row=1, column=1)
    tk.Label(win_client, text='usd', font=('Calibri', 14)).grid(
        row=2, column=1)
    tk.Label(win_client, text='eur', font=('Calibri', 14)).grid(
        row=3, column=1)

    tk.Button(win_client, text='депозит', font=('Calibri', 12), padx=5, command=btn_deposit_click).grid(
        row=4, column=0, stick='we')
    tk.Button(win_client, text='акции', font=('Calibri', 12), padx=5, command=btn_stock_click).grid(
        row=4, column=1, stick='we')
    tk.Button(win_client, text='кредит', font=('Calibri', 12), padx=5, command=btn_loan_click).grid(
        row=4, column=2, stick='we')

    label_name.grid(row=0, column=0, columnspan=3)
    label_rub.grid(row=1, column=0)
    label_usd.grid(row=2, column=0)
    label_eur.grid(row=3, column=0)
    label_usd_b.grid(row=2,column=2)
    label_eur_b.grid(row=3, column=2)

def on_closing_client():
    win_entry.deiconify()
    win_client.destroy()
    cursor.execute("""set role postgres;""")

#Окно deposit 
def btn_deposit_click():
    win_deposit = tk.Toplevel()
    win_deposit.geometry('500x500+100+100')

    cursor.execute(f"""select get_deposit('{N}', '{email}')""")
    list = cursor.fetchall()
    l = str(list[0]).split(",")
    create_date = l[0].strip("(,)'")
    end_date = l[1].strip("(,)'")
    percentage = l[2].strip("(,)'")
    amount = l[3].strip("(,)'")

    label_deposit = tk.Label(win_deposit, text=amount, font=('Calibri', 14), padx=5)
    label_percentage = tk.Label(win_deposit, text=percentage + ' %', font=('Calibri', 14), padx=5)
    label_create = tk.Label(win_deposit, text=create_date.strip('"').split()[:1], font=('Calibri', 14), padx=5)
    label_end = tk.Label(win_deposit, text=end_date.strip('"').split()[:1], font=('Calibri', 14), padx=5)

    tk.Label(win_deposit, text='Депозит', font=('Calibri', 14), padx=5).grid(
        row=0, column=0, sticky='we', columnspan=2)
    tk.Label(win_deposit, text='Дата открытия', font=('Calibri', 14), padx=5).grid(
        row=2, column=0)
    tk.Label(win_deposit, text='Дата закрытия', font=('Calibri', 14), padx=5).grid(
        row=3, column=0)

    label_deposit.grid(row=1, column=0)
    label_percentage.grid(row=1, column=1)
    label_create.grid(row=2, column=1)
    label_end.grid(row=3, column=1)

#Окно кредита
def btn_loan_click():
    win_loan = tk.Toplevel()
    win_loan.geometry('500x500+100+100')

    cursor.execute(f"""select get_loan('{N}', '{email}')""")
    list = cursor.fetchall()
    l = str(list[0]).split(",")
    create_date = l[0].strip("(,)'")
    end_date = l[1].strip("(,)'")
    percentage = l[2].strip("(,)'")
    amount = l[3].strip("(,)'")

    label_deposit = tk.Label(win_loan, text=amount, font=('Calibri', 14), padx=5)
    label_percentage = tk.Label(win_loan, text=percentage + ' %', font=('Calibri', 14), padx=5)
    label_create = tk.Label(win_loan, text=create_date.strip('"').split()[:1], font=('Calibri', 14), padx=5)
    label_end = tk.Label(win_loan, text=end_date.strip('"').split()[:1], font=('Calibri', 14), padx=5)

    tk.Label(win_loan, text='Кредит', font=('Calibri', 14), padx=5).grid(
        row=0, column=0, sticky='we', columnspan=2)
    tk.Label(win_loan, text='Дата открытия', font=('Calibri', 14), padx=5).grid(
        row=2, column=0)
    tk.Label(win_loan, text='Дата закрытия', font=('Calibri', 14), padx=5).grid(
        row=3, column=0)

    label_deposit.grid(row=1, column=0)
    label_percentage.grid(row=1, column=1)
    label_create.grid(row=2, column=1)
    label_end.grid(row=3, column=1)

def select_listbox(event):
    k = str(listbox_stock.curselection())
    l = str(list1[int(k.strip("(',) "))]).split(",")
    stock = str(l[0]).strip("(' ")
    count = str(l[1])
    price = str(l[2])
    stock_b = str(l[3])
    date = str(l[4]).strip("\\\")\'")

    if listbox_stock.get(int(k.strip("(',) "))) == stock:
        label_stock.config(text=stock)
        label_price.config(text=price)
        label_stock_b.config(text=stock_b)
        label_date.config(text=date)
        label_count.config(text=count + ' шт.')

#Окно акций
def btn_stock_click():
    win_stock = tk.Toplevel()
    win_stock.geometry('500x500+100+100')

    cursor.execute(f"""select get_stocks_from_stocks('{N}', '{email}')""")
    global list1
    list1 = cursor.fetchall()

    m_stocks =[]

    for item in list1:
        l = str(item).split(',')[:5]
        l = str(l[0]).strip("(,)'")
        m_stocks.append(l)

    stock = m_stocks[0]
    l = str(list1[0]).split(",")
    count = str(l[1])
    price = str(l[2])
    stock_b = str(l[3])
    date = str(l[4]).strip("\\\")\'")

    global stocks
    stocks = m_stocks
    stocks_var = tk.Variable(value=stocks)

    global listbox_stock
    listbox_stock = tk.Listbox(win_stock, listvariable=stocks_var, font=('Calibri', 10), width=15, selectmode='SINGLE')

    global label_stock, label_price, label_stock_b, label_date, label_count

    label_stock = tk.Label(win_stock, text=stock, font=('Calibri', 11), padx=5)
    label_price = tk.Label(win_stock, text=price, font=('Calibri', 14), padx=5)
    label_stock_b = tk.Label(win_stock, text=stock_b, font=('Calibri', 14), padx=5)
    label_date = tk.Label(win_stock, text=date, font=('Calibri', 14), padx=5)
    label_count = tk.Label(win_stock, text=count + ' шт.', font=('Calibri', 14), padx=5)

    tk.Label(win_stock, text='Акции',  font=('Calibri', 14), padx=5).grid(
        row=0, column=0, columnspan=4, sticky='we')
    tk.Label(win_stock, text='Цена покупки').grid(
        row=2, column=1)
    tk.Label(win_stock, text='Дата покупки').grid(
        row=3, column=1)

    listbox_stock.grid(row=1, column=0, rowspan=3)
    label_stock.grid(row=1, column=1, sticky='w')
    label_price.grid(row=1, column=2)
    label_stock_b.grid(row=2, column=2)
    label_date.grid(row=3, column=2, columnspan=2)
    label_count.grid(row=1, column=3)

    listbox_stock.bind("<<ListboxSelect>>", select_listbox)

#Окно employee
def employee():
    global win_employee
    win_employee = tk.Toplevel()
    win_employee.protocol("WM_DELETE_WINDOW", on_closing_employee)
    win_employee.geometry('500x500+100+100')
    win_entry.withdraw()

    tk.Button(win_employee, text='Персонал', font=('Calibri', 14), padx=5, command=btn_personal_click).grid(
        row=0, column=0, sticky='we')
    tk.Button(win_employee, text='Задания', font=('Calibri', 14), padx=5, command=btn_task_click).grid(
        row=1, column=0, sticky='we')
    tk.Button(win_employee, text='Создать задание', font=('Calibri', 14), padx=5, command=btn_create_task).grid(
        row=2, column=0, sticky='we')
    tk.Button(win_employee, text='Клиенты', font=('Calibri', 14), padx=5, command=btn_ckient1_click).grid(
        row=3, column=0, sticky='we')
    tk.Button(win_employee, text='Отчет по задачам', font=('Calibri', 14), padx=5, command=btn_task_ot).grid(
        row=4, column=0, sticky='we')
    tk.Button(win_employee, text='Отчет по клиентам', font=('Calibri', 14), padx=5, command=btn_client_ot).grid(
        row=5, column=0, sticky='we')

def on_closing_employee():
    win_entry.deiconify()
    win_employee.destroy()
    cursor.execute("""set role postgres;""")

#Окно персонала
def btn_personal_click():
    win_personal = tk.Toplevel()
    win_personal.geometry('1420x600')

    cursor.execute("select * from employees;")
    employees = cursor.fetchall()

    columns = ('employee_uuid', 'employee_fullname', 'login', 'password', 'email_address', 'phone_number')

    table = ttk.Treeview(win_personal, columns=columns, show='headings', height=15)
    table.grid(row=0, column=0, sticky="nsew")
    table.heading('employee_uuid', text='UUID Сотрудника')
    table.heading('employee_fullname', text='ФИО')
    table.heading('login', text='Логин')
    table.heading('password', text='Пароль')
    table.heading('email_address', text='Почта')
    table.heading('phone_number', text='Номер телефона')

    for employee in employees:
        table.insert("", 'end', values=employee)

    scrollbar = ttk.Scrollbar(win_personal, orient='vertical', command=table.yview)
    table.configure(yscroll=scrollbar)
    scrollbar.grid(row=0, column=1, sticky="ns")

#Окно заданий
def btn_task_click():
    win_task = tk.Toplevel()
    win_task.geometry('1420x600')

    cursor.execute("select * from actions;")
    employees = cursor.fetchall()

    columns = ('client_uuid', 'employee_uuid', 'create_date', 'end_date', 'description')

    table = ttk.Treeview(win_task, columns=columns, show='headings', height=15)
    table.grid(row=0, column=0, sticky="nsew")
    table.heading('client_uuid', text='UUID клиента')
    table.heading('employee_uuid', text='UUID персонала')
    table.heading('create_date', text='Время создания')
    table.heading('end_date', text='Время закрытия')
    table.heading('description', text='Описание')

    for employee in employees:
        table.insert("", 'end', values=employee)

    scrollbar = ttk.Scrollbar(win_task, orient='vertical', command=table.yview)
    table.configure(yscroll=scrollbar)
    scrollbar.grid(row=0, column=1, sticky="ns")

#Окно клиентов
def btn_ckient1_click():
    win_client1 = tk.Toplevel()
    win_client1.geometry('1420x600')

    cursor.execute("select * from clients;")
    employees = cursor.fetchall()

    columns = ('client_uuid', 'client_fullname', 'phone_number', 'email_address', 'client_address', 'client_education', 'password')

    table = ttk.Treeview(win_client1, columns=columns, show='headings', height=15)
    table.grid(row=0, column=0, sticky="nsew")
    table.heading('client_uuid', text='UUID клиента')
    table.heading('client_fullname', text='ФИО')
    table.heading('phone_number', text='Номер телефона')
    table.heading('email_address', text='Почта')
    table.heading('client_address', text='Адрес')
    table.heading('client_education', text='Образование')
    table.heading('password', text='Пароль')

    for employee in employees:
        table.insert("", 'end', values=employee)

    scrollbar = ttk.Scrollbar(win_client1, orient='vertical', command=table.yview)
    table.configure(yscroll=scrollbar)
    scrollbar.grid(row=0, column=1, sticky="ns")

    scrollbar2 = ttk.Scrollbar(win_client1, orient='horizontal', command=table.xview)
    table.configure(xscrollcommand=scrollbar2 )
    scrollbar2.grid(row=1, column=0, sticky='we')

#Новое задание
def btn_create_task():
    win_create = tk.Toplevel()
    win_create.geometry('500x500+100+100')

    tk.Label(win_create, text='Имя клиента', font=('Calibri', 14), pady=5).grid(
        row=0, column=0, stick='we')
    tk.Label(win_create, text='Отчество клиента', font=('Calibri', 14), pady=5).grid(
        row=1, column=0, stick='we')
    tk.Label(win_create, text='Фамилия клиента', font=('Calibri', 14), pady=5).grid(
        row=2, column=0, stick='we')
    tk.Label(win_create, text='Почта клиента', font=('Calibri', 14), pady=5).grid(
        row=3, column=0, stick='we')
    tk.Label(win_create, text='Логин', font=('Calibri', 14), pady=5).grid(
        row=4, column=0, stick='we')
    tk.Label(win_create, text='Описание', font=('Calibri', 14), pady=5).grid(
        row=5, column=0, stick='we')
    tk.Label(win_create, text='Дата закрытия', font=('Calibri', 14), pady=5).grid(
        row=6, column=0, stick='we')

    global entry_name1, entry_middle1, entry_surname1, entry_email1, entry_login1, entry_description, entry_end_date

    entry_name1 = tk.Entry(win_create, font=('Calibri', 14))
    entry_middle1 = tk.Entry(win_create, font=('Calibri', 14))
    entry_surname1 = tk.Entry(win_create, font=('Calibri', 14))
    entry_email1 = tk.Entry(win_create, font=('Calibri', 14))
    entry_login1 = tk.Entry(win_create, font=('Calibri', 14))
    entry_description = tk.Entry(win_create, font=('Calibri', 14))
    entry_end_date = tk.Entry(win_create, font=('Calibri', 14))

    entry_name1.grid(row=0, column=1)
    entry_middle1.grid(row=1, column=1)
    entry_surname1.grid(row=2, column=1)
    entry_email1.grid(row=3, column=1)
    entry_login1.grid(row=4, column=1)
    entry_description.grid(row=5, column=1)
    entry_end_date.grid(row=6, column=1)

    tk.Button(win_create, text='Ок', font=('Calibri', 12), command=btn_task_click1).grid(
        row=7, column=1, sticky='e')

#Вносим данные в таблицу actions
def btn_task_click1():

    if (entry_name1.get() != '' and entry_middle1.get() != '' and 
        entry_surname1.get() != '' and entry_email1.get() != '' and 
        entry_login1.get() != '' and entry_description. get() != '' and 
        entry_end_date.get() != ''):

        cursor.execute(
            f"""call task('{entry_surname1.get()} {entry_name1.get()} {entry_middle1.get()}', '{entry_email1.get()}', 
            '{entry_login1.get()}', '{datetime.datetime.now()}', '{entry_end_date.get()}', '{entry_description.get()}');"""
        )

#Отчет по задачам
def btn_task_ot():
    cursor.execute("set role postgres;")
    cursor.execute("SELECT save_report_to_json();")
    success_window = tk.Toplevel()
    success_window.geometry('300x100')
    tk.Label(success_window, text='Отчет по задачам сохранен', font=('Calibri', 14)).pack()
    cursor.execute("set role employee;")

#Отчет по клиентам
def btn_client_ot():
    cursor.execute("set role postgres;")
    cursor.execute("SELECT save_report_to_json_client();")
    success_window = tk.Toplevel()
    success_window.geometry('300x100')
    tk.Label(success_window, text='Отчет по клиентам сохранен', font=('Calibri', 14)).pack()
    cursor.execute("set role employee;")

#Окно входа
win_entry = tk.Tk()
win_entry.title('Банк')
win_entry.geometry('267x200+100+100')
win_entry.resizable(False, False)

tk.Label(win_entry, text='Авторизация', font=('Calibri', 14), pady=5).grid(row=0, column=0, columnspan=2, stick='we')
label_auth = tk.Label(win_entry, text='Почта', font=('Calibri', 14), pady=7)
tk.Label(win_entry, text='Пароль', font=('Calibri', 14), pady=7).grid(row=2, column=0, sticky='we')

entry_login = tk.Entry(win_entry, font=('Calibri', 14), width=15)
entry_password = tk.Entry(win_entry, font=('Calibri', 14), show='*', width=15)

select = tk.IntVar()
select.set(0)
rad_client = tk.Radiobutton(win_entry, text='Клиент', font=('Calibri', 14), variable=select, value=0, command=select_radiobutton).grid(
    row=3, column=0, sticky='w')
rad_employee = tk.Radiobutton(win_entry, text='Сотрудник', font=('Calibri', 14), variable=select, value=1, command=select_radiobutton).grid(
    row=3,column=1, sticky='e')

tk.Button(win_entry, text='Регистрация', font=('Calibri', 12), pady=5, command=btn_reg_click).grid(
    row=4,column=0, sticky='e')
tk.Button(win_entry, text='Вход', font=('Calibri', 12),pady=5, width=5, command=btn_entry_click).grid(
    row=4, column=1, sticky='e')

label_auth.grid(row=1, column=0, sticky='we')
entry_login.grid(row=1, column=1)
entry_password.grid(row=2, column=1)

win_entry.mainloop()