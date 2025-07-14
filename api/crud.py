from api.database import get_connection

def get_top_products(limit=10):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT LOWER(product), COUNT(*) as count
            FROM public.top_products
            WHERE product IS NOT NULL
            GROUP BY LOWER(product)
            ORDER BY count DESC
            LIMIT %s
        """, (limit,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return [{"product": r[0], "count": r[1]} for r in result]
    except Exception as e:
        print("❌ Error in get_top_products:", e)
        return []

def get_channel_activity(channel_name):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DATE(message_date) as date, COUNT(*) as count
            FROM raw.telegram_messages
            WHERE channel_name = %s
            GROUP BY DATE(message_date)
            ORDER BY date
        """, (channel_name,))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return [{"date": str(r[0]), "count": r[1]} for r in result]
    except Exception as e:
        print("❌ Error in get_channel_activity:", e)
        return []


def search_messages(query):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, message_text
            FROM raw.telegram_messages
            WHERE LOWER(message_text) LIKE LOWER(%s)
            LIMIT 100
        """, (f'%{query}%',))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return [{"message_id": r[0], "content": r[1]} for r in results]
    except Exception as e:
        print("❌ Error in search_messages:", e)
        return []
