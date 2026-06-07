from src.rule_engine import RuleEngine

print("Testing Rule Engine...")

engine = RuleEngine()

alerts = engine.check_real_yield()

print("Alerts generated:")
print(alerts)

print("TEST COMPLETE")