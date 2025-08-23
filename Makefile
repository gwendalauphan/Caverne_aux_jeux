.PHONY: help build-linux build-linux-client build-linux-server \
        build-windows build-windows-client build-windows-server \
        run-linux run-linux-client run-linux-server \
        run-windows run-windows-client run-windows-server \
        clean

# Common flags
PYI_COMMON = --onefile --clean --noconfirm --distpath dist --workpath build --specpath .

# Linux add-data uses ":" separator
DATA_LINUX = \
	--add-data "app/Data/*:Data/" \
	--add-data "app/Fantome/Ressources/Images/*:Fantome/Ressources/Images/" \
	--add-data "app/flappy_bird/Ressources/*:flappy_bird/Ressources/" \
	--add-data "app/Minesweeper/Images/*:Minesweeper/Images/" \
	--add-data "app/Parametters/*:Parametters/" \
	--add-data "app/Pendu/ressources/*:Pendu/ressources/" \
	--add-data "app/Pong/res/*:Pong/res/" \
	--add-data "app/Snake/images/*:Snake/images/" \
	--add-data "app/Tete_chercheuse/image/*:Tete_chercheuse/image/" \
	--add-data "app/Tetris/Images/*:Tetris/Images/" \
	--add-data "app/thumbnail/*:thumbnail/"

# Windows add-data uses ";" separator
DATA_WIN = \
	--add-data "app/Data/*;Data/" \
	--add-data "app/Fantome/Ressources/Images/*;Fantome/Ressources/Images/" \
	--add-data "app/flappy_bird/Ressources/*;flappy_bird/Ressources/" \
	--add-data "app/Minesweeper/Images/*;Minesweeper/Images/" \
	--add-data "app/Parametters/*;Parametters/" \
	--add-data "app/Pendu/ressources/*;Pendu/ressources/" \
	--add-data "app/Pong/res/*;Pong/res/" \
	--add-data "app/Snake/images/*;Snake/images/" \
	--add-data "app/Tete_chercheuse/image/*;Tete_chercheuse/image/" \
	--add-data "app/Tetris/Images/*;Tetris/Images/" \
	--add-data "app/thumbnail/*;thumbnail/"

help:
	@echo "Available targets:"
	@echo "  build-linux        Build Linux executables with PyInstaller"
	@echo "  build-linux-debug  Build Linux executables with PyInstaller (debug mode)"
	@echo "  build-windows      Build Windows executables with PyInstaller (run on Windows)"
	@echo "  build-windows-debug  Build Windows executables with PyInstaller (debug mode)"
	@echo "  run-linux          Run Linux server+client"
	@echo "  run-windows        Run Windows server+client"
	@echo "  clean              Remove build artifacts"

define VENV_SETUP
	@if [ ! -d ".make_venv" ]; then \
		python3 -m venv .make_venv; \
	fi
	if [ "$$(uname -s | grep -i 'mingw\|cygwin\|windows')" ]; then \
		. .make_venv/Scripts/activate; \
	else \
		. .make_venv/bin/activate; \
	fi; \
	python -m pip install -r build_requirements.txt -r requirements.txt;
endef

# ---------- Linux ----------
build-linux-client:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) $(DATA_LINUX) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--windowed --noconsole \
		--name main app/main.py; \
	deactivate

build-linux-server:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--windowed --noconsole \
		--add-data "app/Utils/utils.py:Utils/" \
		--name server app/Reseau/server.py; \
	deactivate

build-linux: build-linux-client build-linux-server

# Debug versions (console mode)
build-linux-client-debug:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) $(DATA_LINUX) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--name main app/main.py; \
	deactivate

build-linux-server-debug:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--add-data "app/Utils/utils.py:Utils/" \
		--name server app/Reseau/server.py; \
	deactivate

build-linux-debug: build-linux-client-debug build-linux-server-debug

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
	kill $$SERVER_PID 2>/dev/null || true

# ---------- Windows ----------
build-windows-client:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) $(DATA_WIN) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--windowed --noconsole \
		--name main app/main.py; \
	deactivate

build-windows-server:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--windowed --noconsole \
		--add-data "app/Utils/utils.py;Utils/" \
		--name server app/Reseau/server.py; \
	deactivate

build-windows: build-windows-client build-windows-server

# Debug versions (console mode)
build-windows-client-debug:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) $(DATA_WIN) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--name main app/main.py; \
	deactivate

build-windows-server-debug:
	$(VENV_SETUP) \
	python -m PyInstaller $(PYI_COMMON) $(DATA_WIN) \
		--hidden-import PIL._tkinter_finder --hidden-import platform --hidden-import tkinter.messagebox \
		--add-data "app/Utils/utils.py;Utils/" \
		--name server app/Reseau/server.py; \
	deactivate
	
build-windows-debug: build-windows-client-debug build-windows-server-debug

run-windows-client:
	./dist/main.exe

run-windows-server:
	./dist/server.exe

run-windows:
	@echo "Starting server and client..."
	@./dist/server.exe & \
	SERVER_PID=$$!; \
	powershell -Command "Start-Sleep -Seconds 1" || sleep 1; \
	./dist/main.exe; \
	kill $$SERVER_PID 2>/dev/null || taskkill //PID $$SERVER_PID //F 2>NUL || true

clean:
	rm -rf build dist __pycache__ *.spec .make_venv
