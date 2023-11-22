from console_io import ConsoleIO
from app import App
from services.reference_service import ReferenceService

def main():
    console_io = ConsoleIO()
    reference_service = ReferenceService()
    app = App(console_io, reference_service)

    app.run()


if __name__ == "__main__":
    main()