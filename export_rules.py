from services.rule_exporter import RuleExporter


def main():
    exporter = RuleExporter()
    exporter.export_all()


if __name__ == "__main__":
    main()