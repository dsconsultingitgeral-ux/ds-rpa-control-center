-- =================================================================
-- SCRIPT DE DADOS DE TESTE (POPULAR E LIMPAR)
-- Repositório: ds-rpa-control-center
-- Descrição: Insere 20 execuções simuladas para validação do Streamlit.
-- =================================================================

-- 1. INSERÇÃO DE 20 EXECUÇÕES DE TESTE
INSERT INTO rpa_execucoes 
(id_robot, robot_name, start_time_date, start_time_hour, end_time_date, end_time_hour, duration_seconds, status, error_category, environment, mode, logs) 
VALUES
-- Robô 001: TESTE_FATURACAO
('001', 'TESTE_FATURACAO', '2026-10-10', '08:00:00', '2026-10-10', '08:02:15', 135, 'OK', NULL, 'DEV', 'Agendado', '[08:00:00] Início do processo\n[08:01:10] Processando 5 faturas\n[08:02:15] Concluído com sucesso.'),
('001', 'TESTE_FATURACAO', '2026-10-11', '08:00:00', '2026-10-11', '08:05:30', 330, 'OK', NULL, 'PRD', 'Agendado', '[08:00:00] Início do processo\n[08:03:00] Faturas enviadas\n[08:05:30] Sucesso.'),
('001', 'TESTE_FATURACAO', '2026-10-12', '08:00:00', '2026-10-12', '08:01:45', 105, 'KO', 'Timeout', 'PRD', 'Agendado', '[08:00:00] Início do processo\n[08:01:45] ERRO: Portal das Finanças indisponível (Timeout).'),
('001', 'TESTE_FATURACAO', '2026-10-12', '09:30:00', '2026-10-12', '09:32:00', 120, 'OK', NULL, 'PRD', 'Manual', '[09:30:00] Reexecução manual\n[09:32:00] Sucesso após tentativa.'),
('001', 'TESTE_FATURACAO', '2026-10-13', '08:00:00', '2026-10-13', '08:02:50', 170, 'OK', NULL, 'PRD', 'Agendado', '[08:00:00] Início do processo\n[08:02:50] Processo finalizado OK.'),

-- Robô 002: TESTE_EXTRATOS
('002', 'TESTE_EXTRATOS', '2026-10-10', '09:00:00', '2026-10-10', '09:01:10', 70, 'OK', NULL, 'DEV', 'Manual', '[09:00:00] Login no banco\n[09:01:10] Download do extrato concluído.'),
('002', 'TESTE_EXTRATOS', '2026-10-11', '09:00:00', '2026-10-11', '09:01:15', 75, 'OK', NULL, 'PRD', 'Agendado', '[09:00:00] Login no banco\n[09:01:15] Extrato recolhido.'),
('002', 'TESTE_EXTRATOS', '2026-10-12', '09:00:00', '2026-10-12', '09:00:40', 40, 'KO', 'Login Erro', 'PRD', 'Agendado', '[09:00:00] Login no banco\n[09:00:40] ERRO: Credenciais inválidas ou sessão expirada.'),
('002', 'TESTE_EXTRATOS', '2026-10-13', '09:00:00', '2026-10-13', '09:01:20', 80, 'OK', NULL, 'PRD', 'Agendado', '[09:00:00] Login no banco\n[09:01:20] Extrato OK.'),

-- Robô 003: TESTE_CRM_SYNC
('003', 'TESTE_CRM_SYNC', '2026-10-10', '10:00:00', '2026-10-10', '10:10:00', 600, 'OK', NULL, 'DEV', 'Manual', '[10:00:00] Sincronizando 100 contactos no CRM\n[10:10:00] Concluído.'),
('003', 'TESTE_CRM_SYNC', '2026-10-11', '10:00:00', '2026-10-11', '10:12:30', 750, 'OK', NULL, 'PRD', 'Agendado', '[10:00:00] Sincronizando contactos\n[10:12:30] Sincronização terminada.'),
('003', 'TESTE_CRM_SYNC', '2026-10-12', '10:00:00', '2026-10-12', '10:03:00', 180, 'KO', 'Dados Invalidos', 'PRD', 'Agendado', '[10:00:00] Lendo ficheiro CSV\n[10:03:00] ERRO: Coluna Email em falta no ficheiro de origem.'),
('003', 'TESTE_CRM_SYNC', '2026-10-13', '10:00:00', '2026-10-13', '10:08:15', 495, 'OK', NULL, 'PRD', 'Agendado', '[10:00:00] Sincronização diária\n[10:08:15] OK.'),

-- Robô 004: TESTE_RELATORIO_EMAIL
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-11', '18:00:00', '2026-10-11', '18:00:25', 25, 'OK', NULL, 'PRD', 'Agendado', '[18:00:00] Gerando PDF\n[18:00:25] E-mail enviado à gerência.'),
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-12', '18:00:00', '2026-10-12', '18:00:30', 30, 'OK', NULL, 'PRD', 'Agendado', '[18:00:00] Gerando PDF\n[18:00:30] E-mail enviado à gerência.'),
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-13', '18:00:00', '2026-10-13', '18:00:20', 20, 'KO', 'Falha SMTP', 'PRD', 'Agendado', '[18:00:00] Gerando PDF\n[18:00:20] ERRO: Falha ao ligar ao servidor SMTP.'),

-- Robô 005: TESTE_BACKUP_SISTEMA
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-10', '23:00:00', '2026-10-10', '23:15:00', 900, 'OK', NULL, 'DEV', 'Manual', '[23:00:00] Compactando ficheiros\n[23:15:00] Backup concluído.'),
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-11', '23:00:00', '2026-10-11', '23:14:20', 860, 'OK', NULL, 'PRD', 'Agendado', '[23:00:00] Backup noturno\n[23:14:20] Sucesso.'),
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-12', '23:00:00', '2026-10-12', '23:16:00', 960, 'OK', NULL, 'PRD', 'Agendado', '[23:00:00] Backup noturno\n[23:16:00] Sucesso.'),
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-13', '23:00:00', '2026-10-13', '23:02:10', 130, 'KO', 'Espaco Em Disco', 'PRD', 'Agendado', '[23:00:00] A verificar disco...\n[23:02:10] ERRO: Espaço em disco insuficiente na VM.');


-- =================================================================
-- ⚠️ INSTRUÇÕES DE TRANSIÇÃO PARA PRODUÇÃO (LIMPEZA DE TABELA)
-- =================================================================
-- Quando o cliente entrar em produção ou quiseres apagar os dados de teste,
-- executa os seguintes comandos no SQL Editor do Supabase.
--
-- ATENÇÃO: Isto apagará TODOS os registos de teste e reiniciará o contador ID a partir do 1.
--
-- COMANDOS A EXECUTAR (Descomentar para usar):
--
-- TRUNCATE TABLE rpa_execucoes RESTART IDENTITY;
--
-- =================================================================
