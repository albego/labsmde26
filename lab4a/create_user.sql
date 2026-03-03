-- ============================================
-- CREAR USUARIO CONTENIDO EN LA BASE DE DATOS
-- (no requiere conectarse a master)
-- ============================================

USE [tu_base_de_datos];
GO

-- 1. Crear usuario con contraseña
CREATE USER [nombre_usuario]
WITH PASSWORD = 'Password123!';
GO

-- 2. Asignar permisos (elige el rol que necesites)
ALTER ROLE db_datareader ADD MEMBER [nombre_usuario];  -- solo lectura
-- ALTER ROLE db_datawriter ADD MEMBER [nombre_usuario];  -- escritura
-- ALTER ROLE db_owner     ADD MEMBER [nombre_usuario];  -- control total
GO

-- 3. Verificar que se creó correctamente
SELECT name, type_desc, authentication_type_desc, create_date
FROM sys.database_principals
WHERE name = 'nombre_usuario';
GO
