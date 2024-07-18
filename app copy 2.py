from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

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
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # 사용자 정보 검증
    query = "SELECT * FROM users WHERE username = %s AND user_password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        session['user_id'] = user[0]  # 사용자 ID를 세션에 저장
        flash('로그인 성공!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('로그인 실패. 아이디 또는 비밀번호를 확인하세요.', 'danger')
        return redirect(url_for('login_page'))

# 대시보드
@app.route('/dashboard')
def dashboard():
    # 로그인 여부 확인
    if 'user_id' not in session:
        flash('로그인이 필요합니다.', 'danger')
        return redirect(url_for('login_page'))
    
    # 영화 목록 가져오기
    query = "SELECT * FROM movies"
    cursor.execute(query)
    movies = cursor.fetchall()
    return render_template('dashboard.html', movies=movies)

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

# 상영 시간표 조회
@app.route('/showtimes')
def showtimes():
    # 상영 시간표 정보를 가져옵니다.
    query = "SELECT s.showtime_id, m.title AS movie_title, t.name AS theater_name, s.start_time, s.end_time FROM showtimes s INNER JOIN movies m ON s.movie_id = m.movie_id INNER JOIN theaters t ON s.theater_id = t.theater_id"
    cursor.execute(query)
    showtimes = cursor.fetchall()
    
    return render_template('dashboard.html', showtimes=showtimes)

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('login_page'))

# 메인 코드 실행
if __name__ == '__main__':
    app.run(debug=True)
