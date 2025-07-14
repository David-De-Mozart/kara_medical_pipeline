with raw as (
    select 
        id,
        channel_name,
        lower(regexp_replace(message_text, '[^a-zA-Z0-9\s]', '', 'g')) as cleaned_content
    from {{ source('raw', 'telegram_messages') }}
)

select
    id,
    channel_name,
    cleaned_content,
    unnest(string_to_array(cleaned_content, ' ')) as word
from raw
where cleaned_content != ''
