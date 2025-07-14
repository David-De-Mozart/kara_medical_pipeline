-- models/top_products.sql

WITH cleaned_words AS (
    SELECT
        LOWER(TRIM(word)) AS word
    FROM (
        SELECT
            unnest(
                string_to_array(
                    regexp_replace(cleaned_content, '[^a-zA-Z ]', ' ', 'g'),
                    ' '
                )
            ) AS word
        FROM {{ ref('messages_cleaned') }}
    ) AS all_words
    WHERE LENGTH(TRIM(word)) > 2
)

SELECT
    word AS product,
    COUNT(*) AS mentions
FROM cleaned_words
WHERE word NOT IN (
    'the', 'and', 'for', 'are', 'you', 'with', 'from', 'that', 'this', 'have',
    'your', 'all', 'our', 'can', 'was', 'will', 'has', 'had', 'but', 'not', 'get',
    'more', 'out', 'now', 'new', 'just', 'birr', 'call', 'price', 'only', 'today',
    'in', 'on', 'of', 'as', 'we', 'at', 'to', 'or'
)
GROUP BY word
ORDER BY mentions DESC
LIMIT 100
