-- Добавить телефон к существующему контакту                                                                     
  CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)                   
  LANGUAGE plpgsql AS $$                                                                                           
  BEGIN                                                                                                            
      INSERT INTO phones (contact_id, phone, type)                                                                 
      SELECT id, p_phone, p_type                                                                                   
      FROM contacts                                                                                                
      WHERE name = p_contact_name;                                                                                 
                                                                                                                   
      IF NOT FOUND THEN                                                                                            
          RAISE NOTICE 'Контакт % не найден', p_contact_name;                                                      
      END IF;                                                                                                      
  END;                                                                                                            
  $$;
                                                                                                                   
  -- Переместить контакт в группу (создать группу если не существует)                                              
  CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)                          
  LANGUAGE plpgsql AS $$                                                                                           
  DECLARE                                                                                                          
      v_group_id INT;                                                                                              
  BEGIN                                                                                                            
      -- Ищем группу, если нет — создаём                                                                           
      INSERT INTO groups (name) VALUES (p_group_name)                                                              
      ON CONFLICT (name) DO NOTHING;                                                                               
                                                                                                                   
      SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;                                             
                                                                                                                   
      UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;                                       
                                                                                                                   
      IF NOT FOUND THEN                                                                                            
          RAISE NOTICE 'Контакт % не найден', p_contact_name;                                                      
      END IF;                                                                                                      
  END;                                                                                                             
  $$;                                                                                                             
                                                                                                                   
  -- Поиск по имени, телефону и email                                                                              
  CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)                                                         
  RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR, phone VARCHAR, phone_type  
  VARCHAR) AS $$                                                                                                   
  BEGIN                                                                                                            
      RETURN QUERY                                                                                                 
          SELECT DISTINCT                                                                                          
              c.id, c.name, c.email, c.birthday,                                                                   
              g.name AS group_name,                                                                                
              p.phone, p.type AS phone_type                                                                        
          FROM contacts c                                                                                          
          LEFT JOIN groups g ON c.group_id = g.id                                                                  
          LEFT JOIN phones p ON c.id = p.contact_id                                                                
          WHERE c.name  ILIKE '%' || p_query || '%'                                                                
             OR c.email ILIKE '%' || p_query || '%'                                                                
             OR p.phone ILIKE '%' || p_query || '%'                                                                
          ORDER BY c.name;                                                                                         
  END;                                                                                                             
  $$ LANGUAGE plpgsql; 