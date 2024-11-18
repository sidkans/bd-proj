if __name__ == "__main__":
    import sys
    from microservices.payment_service import PaymentService
    from microservices.order_service import OrderService
    from alerting.alert_manager import AlertManager

    if len(sys.argv) != 2:
        print("Usage: python main.py [service_type]")
        print("Available services: payment, order, alert_manager")
        sys.exit(1)

    service_type = sys.argv[1].lower()

    # Map service_type to their respective classes
    service_mapping = {
        "payment": PaymentService,
        "order": OrderService,
        "alert_manager": AlertManager,
    }

    if service_type in service_mapping:
        service_class = service_mapping[service_type]
        service = service_class()
    else:
        print(f"Unknown service type: {service_type}")
        sys.exit(1)

    try:
        service.start()
    except KeyboardInterrupt:
        print("\nShutting down service...")
        sys.exit(0)
