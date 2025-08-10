.PHONY: help build-linux build-windows run-linux run-windows clean

help:
	@echo "Available targets:"
	@echo "  build-linux    Build Linux executable with PyInstaller"
	@echo "  build-windows  Build Windows executable with PyInstaller (requires Wine or Windows)"
	@echo "  run-linux      Run the Linux executable"
	@echo "  run-windows    Run the Windows executable (requires Wine or Windows)"
	@echo "  clean          Remove build artifacts"

build-linux-client:
	pip install -r requirements.txt
	pyinstaller --onefile \
			--add-data=app/Data/*:Data/ \
			--add-data=app/Fantome/Ressources/Images/*:Fantome/Ressources/Images/ \
			--add-data=app/Flappy_Bird/Ressources/*:Flappy_Bird/Ressources/ \
			--add-data=app/Minesweeper/Images/*:Minesweeper/Images/ \
			--add-data=app/Parametters/*:Parametters/ \
			--add-data=app/Pendu/ressources/*:Pendu/ressources/ \
			--add-data=app/Pong/res/*:Pong/res/ \
			--add-data=app/Snake/images/*:Snake/images/ \
			--add-data=app/Tete_chercheuse/image/*:Tete_chercheuse/image/ \
			--add-data=app/Tetris/Images/*:Tetris/Images/ \
			--add-data=app/thumbnail/*:thumbnail/ \
			--hidden-import=PIL._tkinter_finder --windowed --noconsole app/main.py

build-linux-server:
	pip install -r requirements.txt
	pyinstaller --onefile --windowed --noconsole app/Reseau/server.py

build-linux: build-linux-client build-linux-server


build-windows-client:
	pip install -r requirements.txt
	pyinstaller --onefile \
	--add-data=app/Data/*:Data/ \
	--add-data=app/Fantome/Ressources/Images/*:Fantome/Ressources/Images/ \
	--add-data=app/Flappy_Bird/Ressources/*:Flappy_Bird/Ressources/ \
	--add-data=app/Minesweeper/Images/*:Minesweeper/Images/ \
	--add-data=app/Parametters/*:Parametters/ \
	--add-data=app/Pendu/ressources/*:Pendu/ressources/ \
	--add-data=app/Pong/res/*:Pong/res/ \
	--add-data=app/Snake/images/*:Snake/images/ \
	--add-data=app/Tete_chercheuse/image/*:Tete_chercheuse/image/ \
	--add-data=app/Tetris/Images/*:Tetris/Images/ \
	--add-data=app/thumbnail/*:thumbnail/ \
	--hidden-import=PIL._tkinter_finder --windowed --noconsole app/main.py

build-windows-server:
	pip install -r requirements.txt
	pyinstaller --onefile --windowed --noconsole app/Reseau/server.py

build-windows: build-windows-client build-windows-server

run-linux-client:
	./dist/main

run-linux-server:
	./dist/server

run-linux:
	@echo "Starting server and client..."
	@./dist/server & \
	SERVER_PID=$$!; \
	sleep 1; \
	./dist/main; \
	kill $$SERVER_PID

run-windows-client:
	./dist/main.exe

run-windows-server:
	./dist/server.exe

run-windows:
	@echo "Starting server and client..."
	@./dist/server.exe & \
	SERVER_PID=$$!; \
	sleep 1; \
	./dist/main.exe; \
	kill $$SERVER_PID

clean:
	rm -rf build __pycache__ *.spec
