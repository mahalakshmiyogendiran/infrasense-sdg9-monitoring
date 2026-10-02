def evaluate_reading(vibration, strain, tilt, temperature):
    critical = []
    warning = []

    if vibration > 1.0:
        critical.append("High vibration")
    elif vibration > 0.6:
        warning.append("Increased vibration")

    if strain > 80:
        critical.append("High strain")
    elif strain > 50:
        warning.append("Increased strain")

    if tilt > 4.0:
        critical.append("High tilt")
    elif tilt > 2.0:
        warning.append("Increased tilt")

    if temperature > 50:
        critical.append("High temperature")
    elif temperature > 40:
        warning.append("Increased temperature")

    if critical:
        return "CRITICAL", ", ".join(critical)

    if warning:
        return "WARNING", ", ".join(warning)

    return "SAFE", "All readings are within normal range"