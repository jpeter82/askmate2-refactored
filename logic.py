import db


def get_questions():
    """
    Returns all the questions.
        @return    list    List of dictionaries for each question.
    """
    questions = None
    with db.get_cursor() as cursor:
        sql = """SELECT id,
                        title,
                        message,
                        view_number,
                        vote_number,
                        to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time
                 FROM question
                 ORDER BY submission_time DESC"""
        cursor.execute(sql)
        questions = cursor.fetchall()
    return questions


def user_search(search_phrase):
    """
    Returns search results for user query \n
        @param      search_phrase   string          Phrase providid by the user \n
        @return                     list of dicts   Records that match the search phrase
    """
    records = None
    with db.get_cursor() as cursor:
        data = {'phrase': search_phrase}
        sql = """SELECT q.id AS question_id,
                        REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">',
                                                                                %(phrase)s, '</span>')) AS title,
                        REPLACE(q.message, %(phrase)s, CONCAT('<span class="special-format">', %(phrase)s, '</span>'))
                        AS question_body,
                        q.view_number,
                        q.vote_number AS question_vote,
                        to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                        NULL AS answer_id,
                        NULL AS answer_body,
                        NULL AS answer_date,
                        NULL AS answer_vote
                 FROM question q
                 WHERE q.title ILIKE CONCAT('%%', %(phrase)s, '%%') OR q.message ILIKE CONCAT('%%', %(phrase)s, '%%')

                 UNION ALL

                 SELECT q.id AS question_id,
                        REPLACE(q.title, %(phrase)s, CONCAT('<span class="special-format">',
                                                                                %(phrase)s, '</span>')) AS title,
                        q.message AS question_body,
                        q.view_number,
                        q.vote_number AS question_vote,
                        to_char(q.submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time,
                        a.id AS answer_id,
                        REPLACE(a.message, %(phrase)s, CONCAT('<span class="special-format">',
                                                                                %(phrase)s, '</span>')) AS answer_body,
                        to_char(a.submission_time, 'YYYY-MM-DD HH24:MI') AS answer_date,
                        a.vote_number AS answer_vote
                 FROM question q
                 LEFT OUTER JOIN answer a ON q.id = a.question_id
                 WHERE a.message ILIKE CONCAT('%%', %(phrase)s, '%%')
                 ORDER BY question_id DESC, answer_id DESC;"""
        cursor.execute(sql, data)
        records = cursor.fetchall()
    return records
