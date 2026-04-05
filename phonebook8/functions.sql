CREATE OR REPLACE FUNCTION search_contacts(p text)                                                                                      
  RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$                                                                                
  BEGIN                                                                                                                                   
      RETURN QUERY                                                                                                                        
          SELECT c.id, c.name, c.phone                                                                                                    
          FROM phonebook c                                                                                                                
          WHERE c.name ILIKE '%' || p || '%'                                                                                            
             OR c.phone ILIKE '%' || p || '%';                                                                                            
  END;                                                                                                                                    
  $$ LANGUAGE plpgsql;                                                                                                                    
                                                                                                                                          
                                                                                                                                          
  CREATE OR REPLACE FUNCTION get_contacts_paged(page_number INT, page_size INT)                                                         
  RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
  BEGIN
      RETURN QUERY                                                                                                                        
          SELECT c.id, c.name, c.phone                                                                                                    
          FROM phonebook c                                                                                                                
          ORDER BY c.name                                                                                                                 
          LIMIT page_size                                                                                                                 
          OFFSET (page_number - 1) * page_size;                                                                                         
  END;
  $$ LANGUAGE plpgsql; 