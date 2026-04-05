import csv                                                                                                                              
from connect import get_connection                                                                                                      
                                                                                                                                          
                                                                                                                                          
def search_contacts():                                                                                                                  
      pattern = input("Введите часть имени или телефона: ").strip()                                                                       
                                                                                                                                          
      conn = get_connection()                                                                                                             
      cur = conn.cursor()                                                                                                                 
      cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))                                                                        
      rows = cur.fetchall()                                                                                                               
      cur.close()                                                                                                                         
      conn.close()                                                                                                                        
                                                                                                                                          
      if not rows:                                                                                                                        
          print("Контакты не найдены.")                                                                                                   
      else:                                                                                                                               
          print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")                                                                                   
          print("-" * 40)                                                                                                                 
          for row in rows:                                                                                                                
              print(f"{row[0]:<5} {row[1]:<20} {row[2]}")                                                                                 
                                                                                                                                          
                                                                                                                                          
def show_paged():                                                                                                                       
      page = int(input("Номер страницы: ").strip())                                                                                       
      size = int(input("Контактов на странице: ").strip())                                                                                
                                                                                                                                          
      conn = get_connection()                                                                                                             
      cur = conn.cursor()                                                                                                                 
      cur.execute("SELECT * FROM get_contacts_paged(%s, %s)", (page, size))                                                               
      rows = cur.fetchall()                                                                                                               
      cur.close()                                                                                                                         
      conn.close()                                                                                                                        
                                                                                                                                          
      if not rows:                                                                                                                        
          print("Нет контактов на этой странице.")                                                                                        
      else:                                                                                                                               
          print(f"\n{'ID':<5} {'Имя':<20} {'Телефон'}")                                                                                   
          print("-" * 40)                                                                                                                 
          for row in rows:                                                                                                                
              print(f"{row[0]:<5} {row[1]:<20} {row[2]}")                                                                                 
                                                                                                                                          
                                                                                                                                          
def upsert_contact():                                                                                                                 
      name = input("Введите имя: ").strip()                                                                                               
      phone = input("Введите телефон: ").strip()                                                                                          
                                                                                                                                          
      conn = get_connection()                                                                                                             
      cur = conn.cursor()                                                                                                                 
      cur.execute("CALL upsert_contact(%s, %s)", (name, phone))                                                                           
      conn.commit()                                                                                                                       
      cur.close()                                                                                                                         
      conn.close()                                                                                                                        
      print("Готово!")                                                                                                                    
                                                                                                                                          
                                                                                                                                          
def insert_many():                                                                                                                      
      print("Введите контакты (имя,телефон). Пустая строка — конец.")                                                                     
      names = []                                                                                                                          
      phones = []                                                                                                                         
                                                                                                                                          
      while True:                                                                                                                         
          line = input("Контакт: ").strip()                                                                                               
          if line == "":                                                                                                                  
              break                                                                                                                     
          parts = line.split(",")
          if len(parts) != 2:                                                                                                             
              print("Формат: имя,телефон")                                                                                                
              continue                                                                                                                    
          names.append(parts[0].strip())                                                                                                  
          phones.append(parts[1].strip())                                                                                                 
                                                                                                                                          
      if not names:                                                                                                                       
          print("Ничего не введено.")                                                                                                     
          return                                                                                                                          
                                                                                                                                        
      conn = get_connection()
      cur = conn.cursor()                                                                                                                 
      cur.execute("CALL insert_many_contacts(%s, %s)", (names, phones))                                                                   
      conn.commit()                                                                                                                       
      cur.close()                                                                                                                         
      conn.close()                                                                                                                        
      print("Готово!")                                                                                                                    
                                                                                                                                          
                                                                                                                                          
def delete_contact():                                                                                                                 
      value = input("Введите имя или телефон для удаления: ").strip()
                                                                                                                                          
      conn = get_connection()                                                                                                             
      cur = conn.cursor()                                                                                                                 
      cur.execute("CALL delete_contact(%s)", (value,))                                                                                    
      conn.commit()                                                                                                                       
      cur.close()                                                                                                                       
      conn.close()
      print("Готово!")                                                                                                                    
                                                                                                                                          
                                                                                                                                          
def main():                                                                                                                             
      while True:                                                                                                                         
          print("\n=== PhoneBook 8 ===")                                                                                                
          print("1. Поиск контакта")                                                                                                      
          print("2. Показать постранично")                                                                                                
          print("3. Добавить / обновить контакт")                                                                                         
          print("4. Добавить много контактов")                                                                                            
          print("5. Удалить контакт")                                                                                                     
          print("6. Выход")                                                                                                               
                                                                                                                                          
          choice = input("Выбор: ").strip()                                                                                               
                                                                                                                                          
          if choice == "1":                                                                                                               
              search_contacts()                                                                                                         
          elif choice == "2":
              show_paged()
          elif choice == "3":
              upsert_contact()                                                                                                            
          elif choice == "4":                                                                                                             
              insert_many()                                                                                                               
          elif choice == "5":                                                                                                             
              delete_contact()                                                                                                            
          elif choice == "6":                                                                                                           
              break
          else:
              print("Неверный выбор.")                                                                                                    
                                                                                                                                          
                                                                                                                                          
if __name__ == "__main__":                                                                                                              
      main() 