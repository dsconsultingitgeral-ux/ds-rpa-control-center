-- =================================================================
-- SCRIPT DE DADOS DE TESTE (20 EXECUÇÕES COMPLETAS)
-- Repositório: ds-rpa-control-center
-- =================================================================

-- 1. Limpeza prévia (Garante tabela limpa e reinicia IDs a partir de 1)
TRUNCATE TABLE rpa_execucoes RESTART IDENTITY;

-- 2. Inserção das 20 execuções simuladas
INSERT INTO rpa_execucoes 
(id_robot, robot_name, start_time_date, start_time_hour, end_time_date, end_time_hour, duration_seconds, status, error_category, environment, mode, logs) 
VALUES

-- [Execução 1] Robô 001 - Faturação (Sucesso, PRD, Agendado, Log Longo)
('001', 'TESTE_FATURACAO', '2026-10-12', '08:00:00', '2026-10-12', '08:08:45', 525, 'OK', NULL, 'PRD', 'Agendado', 
'[08:00:00] [INFO] Inicializando o OpenRPA Engine v24.2...
[08:00:02] [INFO] A carregar credenciais seguras do cofre...
[08:00:05] [INFO] A ligar ao portal de faturação externo (https://faturas.exemplo.pt)...
[08:00:12] [INFO] Autenticação efetuada com sucesso para o utilizador "rpa_bot_01".
[08:00:25] [INFO] A ler ficheiro de origem "lote_faturas_outubro.xlsx" (Total: 45 registos).
[08:00:30] [INFO] [Registo 01/45] Processando contribuinte 509123456...
[08:00:45] [INFO] [Registo 01/45] Fatura emitida com sucesso. ID: FT-2026/891.
[08:01:10] [WARN] [Registo 02/45] Resposta lenta do servidor de destino (>20s). A aguardar...
[08:01:35] [INFO] [Registo 02/45] Fatura emitida com sucesso. ID: FT-2026/892.
[08:07:30] [INFO] [Registo 43 a 45/45] Últimos registos processados com sucesso.
[08:08:45] [INFO] Processo concluído com sucesso. Estado final: OK.'),

-- [Execução 2] Robô 001 - Faturação (Erro, PRD, Agendado)
('001', 'TESTE_FATURACAO', '2026-10-13', '08:00:00', '2026-10-13', '08:01:45', 105, 'KO', 'Timeout', 'PRD', 'Agendado', 
'[08:00:00] [INFO] Inicializando o OpenRPA Engine...
[08:00:02] [INFO] A ligar ao portal de faturação...
[08:01:45] [CRITICAL] ERRO FATAL: O elemento "BotaoSubmeterLote" não foi encontrado no ecrã após 60s.
[08:01:45] [ERROR] Processo interrompido abruptamente. Estado final: KO.'),

-- [Execução 3] Robô 001 - Faturação (Sucesso, PRD, Manual - Reexecução)
('001', 'TESTE_FATURACAO', '2026-10-13', '09:30:00', '2026-10-13', '09:32:10', 130, 'OK', NULL, 'PRD', 'Manual', 
'[09:30:00] [INFO] Arranque manual pelo operador.
[09:30:15] [INFO] A re-submeter o lote pendente...
[09:32:10] [INFO] Processo concluído com sucesso após reexecução manual.'),

-- [Execução 4] Robô 001 - Faturação (Sucesso, DEV, Manual)
('001', 'TESTE_FATURACAO', '2026-10-14', '11:00:00', '2026-10-14', '11:02:00', 120, 'OK', NULL, 'DEV', 'Manual', 
'[11:00:00] [INFO] Teste de script em ambiente DEV.
[11:02:00] [INFO] Testes unitários validados com sucesso.'),

-- [Execução 5] Robô 001 - Faturação (Sucesso, PRD, Agendado)
('001', 'TESTE_FATURACAO', '2026-10-15', '08:00:00', '2026-10-15', '08:03:15', 195, 'OK', NULL, 'PRD', 'Agendado', 
'[08:00:00] [INFO] Execução agendada iniciada.
[08:03:15] [INFO] 20 faturas processadas. OK.'),

-- [Execução 6] Robô 002 - Extratos (Sucesso, PRD, Agendado)
('002', 'TESTE_EXTRATOS', '2026-10-12', '09:00:00', '2026-10-12', '09:01:10', 70, 'OK', NULL, 'PRD', 'Agendado', 
'[09:00:00] [INFO] A iniciar extração de movimentos bancários.
[09:00:10] [INFO] Acedendo ao homebanking...
[09:01:10] [INFO] Ficheiro OFX descarregado com sucesso.'),

-- [Execução 7] Robô 002 - Extratos (Erro, PRD, Agendado)
('002', 'TESTE_EXTRATOS', '2026-10-13', '09:00:00', '2026-10-13', '09:00:45', 45, 'KO', 'Login Erro', 'PRD', 'Agendado', 
'[09:00:00] [INFO] A iniciar extração de movimentos bancários.
[09:00:45] [ERROR] ERRO: Falha na autenticação de dois fatores (2FA) do banco. Sessão terminada.'),

-- [Execução 8] Robô 002 - Extratos (Sucesso, PRD, Manual)
('002', 'TESTE_EXTRATOS', '2026-10-13', '10:15:00', '2026-10-13', '10:16:15', 75, 'OK', NULL, 'PRD', 'Manual', 
'[10:15:00] [INFO] Nova tentativa manual de extração de extratos.
[10:16:15] [INFO] Extrato recolhido e colocado na pasta de rede. OK.'),

-- [Execução 9] Robô 002 - Extratos (Sucesso, DEV, Manual)
('002', 'TESTE_EXTRATOS', '2026-10-14', '14:00:00', '2026-10-14', '14:01:00', 60, 'OK', NULL, 'DEV', 'Manual', 
'[14:00:00] [INFO] Validação de seletores web em DEV.
[14:01:00] [INFO] Teste concluído.'),

-- [Execução 10] Robô 002 - Extratos (Sucesso, PRD, Agendado)
('002', 'TESTE_EXTRATOS', '2026-10-15', '09:00:00', '2026-10-15', '09:01:05', 65, 'OK', NULL, 'PRD', 'Agendado', 
'[09:00:00] [INFO] Execução diária de extratos.
[09:01:05] [INFO] Concluído sem incidências.'),

-- [Execução 11] Robô 003 - CRM Sync (Sucesso, DEV, Manual)
('003', 'TESTE_CRM_SYNC', '2026-10-12', '10:00:00', '2026-10-12', '10:10:00', 600, 'OK', NULL, 'DEV', 'Manual', 
'[10:00:00] [INFO] Sincronização inicial de contactos em DEV.
[10:10:00] [INFO] 100 contactos sincronizados.'),

-- [Execução 12] Robô 003 - CRM Sync (Erro, PRD, Agendado)
('003', 'TESTE_CRM_SYNC', '2026-10-13', '10:00:00', '2026-10-13', '10:03:00', 180, 'KO', 'Dados Invalidos', 'PRD', 'Agendado', 
'[10:00:00] [INFO] Sincronização diária com o CRM.
[10:02:50] [WARN] Linha 12: Formato de telemóvel inválido.
[10:03:00] [ERROR] ERRO: O campo obrigatório "Email" está vazio na linha 15. Sincronização cancelada.'),

-- [Execução 13] Robô 003 - CRM Sync (Sucesso, PRD, Agendado)
('003', 'TESTE_CRM_SYNC', '2026-10-14', '10:00:00', '2026-10-14', '10:08:30', 510, 'OK', NULL, 'PRD', 'Agendado', 
'[10:00:00] [INFO] Sincronização após correção do ficheiro de origem.
[10:08:30] [INFO] Sincronização concluída com sucesso. 98 registos atualizados.'),

-- [Execução 14] Robô 003 - CRM Sync (Sucesso, PRD, Agendado)
('003', 'TESTE_CRM_SYNC', '2026-10-15', '10:00:00', '2026-10-15', '10:07:45', 465, 'OK', NULL, 'PRD', 'Agendado', 
'[10:00:00] [INFO] Sincronização diária PRD.
[10:07:45] [INFO] Sucesso.'),

-- [Execução 15] Robô 004 - Relatório Email (Sucesso, PRD, Agendado)
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-12', '18:00:00', '2026-10-12', '18:00:25', 25, 'OK', NULL, 'PRD', 'Agendado', 
'[18:00:00] [INFO] A gerar relatório diário em PDF...
[18:00:25] [INFO] E-mail enviado com sucesso para a diretoria.'),

-- [Execução 16] Robô 004 - Relatório Email (Sucesso, PRD, Agendado)
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-13', '18:00:00', '2026-10-13', '18:00:30', 30, 'OK', NULL, 'PRD', 'Agendado', 
'[18:00:00] [INFO] A gerar relatório diário em PDF...
[18:00:30] [INFO] E-mail enviado com sucesso.'),

-- [Execução 17] Robô 004 - Relatório Email (Erro, PRD, Agendado)
('004', 'TESTE_RELATORIO_EMAIL', '2026-10-14', '18:00:00', '2026-10-14', '18:00:20', 20, 'KO', 'Falha SMTP', 'PRD', 'Agendado', 
'[18:00:00] [INFO] A gerar relatório em PDF...
[18:00:20] [ERROR] ERRO: Falha de conexão ao servidor SMTP de envio de correio.'),

-- [Execução 18] Robô 005 - Backup Sistema (Sucesso, DEV, Manual)
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-12', '23:00:00', '2026-10-12', '23:15:00', 900, 'OK', NULL, 'DEV', 'Manual', 
'[23:00:00] [INFO] Teste de rotina de backup em DEV.
[23:15:00] [INFO] Ficheiros compactados com sucesso.'),

-- [Execução 19] Robô 005 - Backup Sistema (Sucesso, PRD, Agendado)
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-13', '23:00:00', '2026-10-13', '23:14:20', 860, 'OK', NULL, 'PRD', 'Agendado', 
'[23:00:00] [INFO] Backup noturno automático iniciado.
[23:14:20] [INFO] Cópia de segurança transferida para o storage externo com sucesso.'),

-- [Execução 20] Robô 005 - Backup Sistema (Erro, PRD, Agendado)
('005', 'TESTE_BACKUP_SISTEMA', '2026-10-14', '23:00:00', '2026-10-14', '23:02:10', 130, 'KO', 'Espaco Em Disco', 'PRD', 'Agendado', 
'[23:00:00] [INFO] A iniciar backup noturno...
[23:02:10] [ERROR] ERRO: Espaço em disco insuficiente na drive C: da VM para criar a imagem temporária.');
