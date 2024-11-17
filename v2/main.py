if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py [service_type]")
        print("Available services: payment, order, inventory, alert_manager")
        sys.exit(1)

    service_type = sys.argv[1].lower()

    if service_type == "payment":
        service = PaymentService()
    elif service_type == "alert_manager":
        service = AlertManager()
    else:
        print(f"Unknown service type: {service_type}")
        sys.exit(1)

    try:
        service.start()
    except KeyboardInterrupt:
        print("\nShutting down service...")
        sys.exit(0)