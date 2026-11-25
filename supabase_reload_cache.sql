-- Execute no Supabase SQL Editor (SQL Editor > New Query > Run)
-- Recarrega o schema cache do PostgREST após ALTER TABLE / CREATE TABLE.
-- Sem isso, a API REST não reconhece colunas novas (erro PGRST204).

NOTIFY pgrst, 'reload schema';

-- Depois de executar, rode novamente:
--   python supabase_quick_start.py
-- ou dê duplo clique em:
--   atualizar_stats.bat
