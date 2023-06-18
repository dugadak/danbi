# danbi 프로젝트
 실행방법
 메일로 수신된 docker-compose.yml를
다운 받은 danbi 프로젝트에,
secret_settings.py를 danbi프로젝트 안 danbi앱에 넣고,
 docker-compose up 후 danbi-web 컨테이너 접속.
접속 후 python -m venv venv로 가상환경 생성,
생성된 가상환경에 접속 후
pip install -r requirements.txt로 해당 라이브러리 설치.
 python manage.py migrate로 마이그레이션 후 python manage.py runserver로 서버 가동.
 
 테스트 코드는
python manage.py test [해당 앱]으로 확인 가능
 ex) python manage.py User
 
 주의할점
 Team 7개의 데이터가 필요함.
 단비, 다래, 블라블라, 철로, 땅이, 해태, 수피
