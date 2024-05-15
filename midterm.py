import os
import pack.modu as lib

if not os.path.exists('library.db'):
    lib.create_database()
    read_users_file = lib.read_users_file('users.csv')
    read_books_file = lib.read_books_file('books.json')
else:
    read_users_file = lib.users_records('users.csv')
    read_books_file = lib.books_records('books.json')

if read_users_file != 'error' and read_books_file != 'error':
    while True:
        authenticate_user = lib.authenticate_user()
        if authenticate_user == 'error':
            break
        elif authenticate_user is True:
            break

    if authenticate_user is True:
        while True:
            lib.display_menu()
            choice = input("選擇要執行的功能(Enter離開)：")
            if choice == "1":
                lib.add_record()
            elif choice == "2":
                lib.delete_record()
            elif choice == "3":
                lib.modify_record()
            elif choice == "4":
                lib.query_record()
            elif choice == "5":
                lib.list_records()
            elif choice == "":
                print("程式結束")
                break
            else:
                print("=>無效的選擇")
