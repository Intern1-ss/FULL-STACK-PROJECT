import csv
from student.models import State, District  # Ensure models are correctly imported

def run():
    try:
        with open('states_and_districts.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                state_name = row['State'].strip()
                district_name = row['District'].strip()

                # Create or get the State object
                state, created_state = State.objects.get_or_create(name=state_name)
                if created_state:
                    print(f"🆕 State created: {state_name}")

                # Create or get the District object linked to the state
                district, created_district = District.objects.get_or_create(
                    state=state,
                    name=district_name
                )
                if created_district:
                    print(f"🆕 District created: {district_name} (State: {state_name})")

        print("\n✅ Import completed successfully.")

    except FileNotFoundError:
        print("❌ CSV file not found. Please make sure 'states_and_districts.csv' is in the correct location.")

    except Exception as e:
        print(f"❌ Error occurred during import: {e}")
