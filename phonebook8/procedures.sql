CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)                                                             
  LANGUAGE plpgsql AS $$                                                                                                                  
  BEGIN                                                                                                                                   
      IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN                                                                        
          UPDATE phonebook SET phone = p_phone WHERE name = p_name;                                                                       
      ELSE                                                                                                                                
          INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);                                                                     
      END IF;                                                                                                                             
  END;                                                                                                                                    
  $$;                                                                                                                                     
                                                                                                                                          
                                                                                                                                          
  CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names VARCHAR[], p_phones VARCHAR[])                                                 
  LANGUAGE plpgsql AS $$                                                                                                                  
  DECLARE                                                                                                                                 
      i INT;                                                                                                                            
      bad_data TEXT := '';                                                                                                                
  BEGIN                                                                                                                                   
      FOR i IN 1..array_length(p_names, 1) LOOP                                                                                           
          IF p_phones[i] ~ '^\+?[0-9 ]{7,20}$' THEN                                                                                       
              CALL upsert_contact(p_names[i], p_phones[i]);                                                                               
          ELSE                                                                                                                            
              bad_data := bad_data || p_names[i] || ': ' || p_phones[i] || E'\n';                                                         
          END IF;                                                                                                                         
      END LOOP;                                                                                                                           
                                                                                                                                          
      IF bad_data <> '' THEN                                                                                                              
          RAISE NOTICE 'Некорректные данные:%', bad_data;                                                                                 
      END IF;                                                                                                                             
  END;                                                                                                                                    
  $$;                                                                                                                                     
                                                                                                                                          
                                                                                                                                        
  CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
  LANGUAGE plpgsql AS $$
  BEGIN                                                                                                                                   
      IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_value) THEN                                                                       
          DELETE FROM phonebook WHERE name = p_value;                                                                                     
      ELSIF EXISTS (SELECT 1 FROM phonebook WHERE phone = p_value) THEN                                                                   
          DELETE FROM phonebook WHERE phone = p_value;                                                                                    
      ELSE                                                                                                                                
          RAISE NOTICE 'Контакт не найден: %', p_value;                                                                                   
      END IF;                                                                                                                             
  END;                                                                                                                                    
  $$;