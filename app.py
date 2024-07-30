from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 세션을 위한 비밀키 설정

# MySQL 연결 설정
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",  # 비밀번호 설정 필요
    database="movie_book"
)
cursor = db_connection.cursor()

# 로그인 페이지
@app.route('/')
def login_page():
    return render_template('login.html')

# 로그인 처리
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['user_id']
#     password = request.form['password']

#     query = "SELECT user_password FROM users WHERE username = %s"
#     cursor.execute(query, (username,))
#     result = cursor.fetchone()

#     if result and check_password_hash(result[0], password):
#         session['user_id'] = username # 또는 user_id 사용
#         flash('로그인 성공!', 'success')
#         return redirect(url_for('dashboard'))
#     else:
#         flash('로그인 실패. 아이디 또는 비밀번호를 확인하세요.', 'danger')
#         return redirect(url_for('login_page'))
@app.route('/login', methods=['POST'])
def login():
    username = request.form['user_id']
    password = request.form['password']

    query = "SELECT user_id, user_password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result and check_password_hash(result[1], password):
        session['user_id'] = result[0]  # 실제 user_id를 세션에 저장
        flash('로그인 성공!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('로그인 실패. 아이디 또는 비밀번호를 확인하세요.', 'danger')
        return redirect(url_for('login_page'))




# 회원가입 페이지
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# 회원가입 처리
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash('이미 사용 중인 사용자 이름입니다.', 'danger')
            return redirect(url_for('register_page'))

        insert_query = "INSERT INTO users (username, user_password, email) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (username, hashed_password, email))
        db_connection.commit()

        flash('회원가입이 완료되었습니다. 로그인해 주세요.', 'success')
        return redirect(url_for('login_page'))

    except mysql.connector.Error as err:
        db_connection.rollback()
        flash(f'회원가입 중 오류가 발생했습니다: {err}', 'danger')
        return redirect(url_for('register_page'))



# 대시보드
@app.route('/dashboard')
def dashboard():
    # 로그인 여부 확인
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login_page'))
    
    user_id = session['user_id']
    
    # 영화 목록 가져오기
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    
    # 상영 시간표 목록 가져오기
    query = """
    SELECT s.showtime_id, m.title AS movie_title, t.theater_name AS theater_name, s.start_time, s.end_time 
    FROM showtimes s 
    INNER JOIN movies m ON s.movie_id = m.movie_id 
    INNER JOIN theaters t ON s.theater_id = t.theater_id
    """
    cursor.execute(query)
    showtimes = cursor.fetchall()

    # 예약 목록 가져오기
    query = """
    SELECT r.reservation_id, m.title, t.theater_name, s.start_time, se.seat_number, r.pay_status
    FROM reservations r
    JOIN showtimes s ON r.showtime_id = s.showtime_id
    JOIN movies m ON s.movie_id = m.movie_id
    JOIN theaters t ON s.theater_id = t.theater_id
    JOIN seats se ON r.seat_id = se.seat_id
    WHERE r.user_id = %s
    """
    cursor.execute(query, (user_id,))
    reservations = cursor.fetchall()

    
    return render_template('dashboard.html', movies=movies, showtimes=showtimes, reservations=reservations)




# 좌석 정보 가져오기
@app.route('/seats/<int:showtime_id>')
def seats(showtime_id):
    # 상영 시간표의 상영관 정보를 가져옵니다
    showtime_query = "SELECT theater_id FROM showtimes WHERE showtime_id = %s"
    cursor.execute(showtime_query, (showtime_id,))
    result = cursor.fetchone()
    if not result:
        return "상영 시간표를 찾을 수 없습니다.", 404

    theater_id = result[0]

    # 해당 상영관의 좌석 정보만 가져옵니다
    query = """
    SELECT se.seat_id, se.seat_number, 
           CASE WHEN re.seat_id IS NOT NULL THEN 1 ELSE 0 END AS reserved
    FROM seats se
    LEFT JOIN reservations re ON se.seat_id = re.seat_id AND re.showtime_id = %s
    WHERE se.theater_id = %s
    """
    cursor.execute(query, (showtime_id, theater_id))
    seats = cursor.fetchall()
    
    seat_buttons_html = ""
    for seat in seats:
        seat_id, seat_number, reserved = seat
        button_class = "seat-button"
        if reserved:
            button_class += " reserved"
        seat_buttons_html += f'<button class="{button_class}" value="{seat_id}">{seat_number}</button>'
    
    return seat_buttons_html




# 좌석 예약 처리
@app.route('/reserve', methods=['POST'])
def reserve():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login_page'))
    
    user_id = int(session['user_id'])
    showtime_id = int(request.form['showtime_id'])
    seat_ids = request.form.get('seat_ids')  # 문자열로 받아옴
    seat_ids = json.loads(seat_ids)  # JSON 문자열을 리스트로 변환
    seat_ids = [int(seat_id) for seat_id in seat_ids]  # 정수형으로 변환

    print('Received seat_ids:', seat_ids)  # 디버깅용

    try:
        for seat_id in seat_ids:
            # 이미 예약된 좌석인지 확인
            check_query = "SELECT * FROM reservations WHERE showtime_id = %s AND seat_id = %s"
            cursor.execute(check_query, (showtime_id, seat_id))
            if cursor.fetchone():
                flash(f'이미 예약된 좌석이 포함되어 있습니다. 다시 선택해주세요.', 'danger')
                return redirect(url_for('dashboard'))
            
            # 좌석 예약 처리
            insert_query = "INSERT INTO reservations (showtime_id, user_id, seat_id, reservation_time, pay_status) VALUES (%s, %s, %s, NOW(), 'unpaid')"
            cursor.execute(insert_query, (showtime_id, user_id, seat_id))
        
        db_connection.commit()  # 트랜잭션 커밋
        flash('좌석이 예약되었습니다.', 'success')
    except mysql.connector.Error as err:
        db_connection.rollback()  # 롤백
        # 로그 추가: 오류 메시지 출력
        app.logger.error(f"Database error: {err}")
        flash(f'예약 중 오류가 발생했습니다: {err}', 'danger')
    
    return redirect(url_for('dashboard'))







# 검색 기능 구현
@app.route('/search')
def search():
    search_text = request.args.get('search_text', '')
    
    # 검색어를 포함하는 영화 조회
    query = "SELECT * FROM movies WHERE title LIKE %s"
    cursor.execute(query, ('%' + search_text + '%',))
    movies = cursor.fetchall()
    
    # 검색 결과를 HTML 형식으로 반환
    movie_html = ''
    for movie in movies:
        movie_html += '<div class="card mb-3">'
        movie_html += '<div class="card-body">'
        movie_html += '<h5 class="card-title">{}</h5>'.format(movie[1])  # movie[1]은 제목을 가정
        movie_html += '<p class="card-text">{}</p>'.format(movie[2])  # movie[2]은 설명을 가정
        movie_html += '<p class="card-text"><small class="text-muted">장르: {}, 상영 시간: {}분</small></p>'.format(movie[3], movie[4])  # movie[3]은 장르, movie[4]는 상영 시간을 가정
        movie_html += '</div></div>'
    
    return movie_html




# 결제 처리
@app.route('/pay', methods=['POST'])
def pay():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login_page'))

    reservation_id = int(request.form['reservation_id'])

    try:
        update_query = "UPDATE reservations SET pay_status = 'paid' WHERE reservation_id = %s"
        cursor.execute(update_query, (reservation_id,))
        db_connection.commit()
        flash('결제가 완료되었습니다.', 'success')
    except mysql.connector.Error as err:
        db_connection.rollback()
        flash(f'결제 중 오류가 발생했습니다: {err}', 'danger')

    return redirect(url_for('dashboard'))

# 예매 취소 처리
@app.route('/cancel', methods=['POST'])
def cancel():
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login_page'))

    reservation_id = int(request.form['reservation_id'])

    try:
        delete_query = "DELETE FROM reservations WHERE reservation_id = %s"
        cursor.execute(delete_query, (reservation_id,))
        db_connection.commit()
        flash('예매가 취소되었습니다.', 'success')
    except mysql.connector.Error as err:
        db_connection.rollback()
        flash(f'예매 취소 중 오류가 발생했습니다: {err}', 'danger')

    return redirect(url_for('dashboard'))





# 로그아웃!
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('login_page'))

# 메인 코드 실행
if __name__ == '__main__':
    app.run(debug=True)



