import os
import datetime
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Credenciais do Supabase não encontradas nas variáveis de ambiente.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Consulta o registo com ID 1
res = supabase.table("rpa_execucoes").select("start_time_date").eq("id", 1).execute()

if res.data:
    data_atual_str = res.data[0]["start_time_date"]
    data_atual = datetime.datetime.strptime(data_atual_str, "%Y-%m-%d").date()
    nova_data = (data_atual + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Atualiza somando +1 dia
    supabase.table("rpa_execucoes").update({"start_time_date": nova_data}).eq("id", 1).execute()
    print(f"✅ ID 1 atualizado com sucesso! Nova data: {nova_data}")
else:
    print("❌ Registo com ID 1 não encontrado.")
