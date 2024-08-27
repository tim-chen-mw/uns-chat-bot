import json
import random
import string
from datetime import datetime, timedelta
import uuid

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def random_string(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=length))

def generate_timestamp(start_time, end_time):
    """
    Generate a random timestamp between two given datetime objects.
    """
    time_range = end_time - start_time
    random_seconds = random.randint(0, int(time_range.total_seconds()))
    return start_time + timedelta(seconds=random_seconds)

def generate_oee(now = datetime.now()):
    availability = random.uniform(0.1, 1)
    performance = random.uniform(0.1, 1)
    quality = random.uniform(0.1, 1)
    oee =  availability*performance*quality
    oee = {
            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
            "Availability": availability,
            "Performance": performance,
            "Quality": quality,
            "OEE": oee
        }
    return oee

def generate_packaging_data():
    now = datetime.now()
    simulated_data = {
        "packaging": {   
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuanity": random.randint(100, 1000),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": random.choice(["Vegetarian", "Non-Vegetarian", "Vegan"])
            },
            "MES": {
                "production": {
                    "jobStatus": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.randint(0, 1)),
                    },
                    "jobStartTime": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": (now + timedelta(days=1, hours=1)).strftime("%m/%d/%Y %H:%M:%S"),
                    },
                    "jobEndTime": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": (now + timedelta(days=1, hours=4)).strftime("%m/%d/%Y %H:%M:%S"),
                    },
                    "rejectedQuantity": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.randint(0, 10)),
                    },
                    "producedQuantity": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.randint(200, 300)),
                    }
                },
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    }
                },
                "quality": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "OrderNumber": random.randint(100000, 999999),
                    "AcceptanceQuantity": random.randint(100, 250),
                    "RejectionQuantity": random.randint(0, 50),
                    "TestingParameters": None
                },
                "maintenanceStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": random.randint(0, 1)
                }              
            },
            "CMMS": {
                "maintenanceJobList": [
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "machineId": "PWR001",
                        "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                        "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                        "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                        "maintenanceType": random.choice(["preventive", "corrective"]),
                        "maintenanceTechnician": random.choice([None, random_string(5)])
                    }
                ]              
            },
            "RCA006": {
            "informations": {
                "type": "RoomClimateAnalyzer",
                "manufacturer": "AirMasters",
                "modelYear": str(random.randint(2015, 2022)),
                "serialNumber": f"RCA{random_string(5)}",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "RCA006",
                
            },
            "machineData": {
                "ambiantHumidity": {
                    "value": random.randint(70, 90),
                    "unit": "%"
                },
                "ambiantTemperature": {
                    "value": random.randint(10, 18),
                    "unit": "°C"
                }
            }
            },
            "PWR001": {
                "informations": {
                    "type": "PizzaWrappingMachine",
                    "manufacturer": "mwPizza",
                    "modelYear": str(random.randint(2020, 2023)),
                    "serialNumber": f"PWR{random_string(5)}",
                    "capacity": random.randint(500, 1500),
                    "capacityUnit": "pieces/hour",
                    "ratedPower": "3000 WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "PWR001",
                },
                "machineData": { 
                    "machineStatus": {
                        "value": random.randint(0, 1),
                        "unit": "integer",
                        "description": "Machine status. Running = 1, Stopped = 0",
                        "timestamp": now.isoformat(),
                    },
                    "counter": {
                        "value": random.randint(1000, 10000),
                        "unit": "pieces",
                        "description": "Total weight of product in kneading machine",
                        "timestamp": now.isoformat(),
                    },
                    "wrapMaterial": {
                        "value": random.choice(["POF", "PVC"]),
                        "unit": "material",
                        "description": "Type of wrap material used",
                        "timestamp": now.isoformat(),
                    },
                    "wrapThickness": {
                        "value": round(random.uniform(0.01, 0.02), 3),
                        "unit": "mm",
                        "description": "Thickness of wrap material",
                        "timestamp": now.isoformat(),
                    },
                    "conveyorSpeed": {
                        "value": random.randint(10, 100),
                        "unit": "cm/s",
                        "description": "Current speed of the conveyor belt",
                        "timestamp": now.isoformat(),
                    },
                    "shrinkHeaterTemperature": {
                        "value": random.randint(50, 150),
                        "unit": "°C",
                        "description": "Temperature inside the shrink foil heater",
                        "timestamp": now.isoformat(),
                    },
                    "alarms": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": random.choice(["KneadingTimeExceeded", "TemperatureTooHigh"]),
                            "alarmStatus": random.choice(["Cleared", "Active"]),
                            "machineId": "KM001",
                        },
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": random.choice(["KneadingTimeExceeded", "TemperatureTooHigh"]),
                            "alarmStatus": random.choice(["Cleared", "Active"]),
                            "machineId": "KM001",
                        }
                    ]
                }
            },
            "PBM001": {
                "informations": {
                    "type": "SecondaryPackagingMachine",
                    "manufacturer": "PackTech",
                    "modelYear": str(random.randint(2015, 2020)),
                    "serialNumber": f"SPM{random_string(5)}",
                    "capacity": random.randint(500, 1000),
                    "capacityUnit": "pcs/hour",
                    "ratedPower": "3500 WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "SPM001",
                },
                "machineData": {
                    "machineStatus": {
                        "value": random.randint(0, 1),
                        "unit": "integer",
                        "description": "Machine status. Running = 1, Stopped = 0",
                        "timestamp": now.isoformat(),
                    },
                    "boxType": {
                        "value": "Cardboard",
                        "unit": "material",
                        "description": "Type of box used",
                        "timestamp": now.isoformat(),
                    },
                    "boxDimensions": {
                        "length": random.randint(20, 40),
                        "width": random.randint(20, 40),
                        "height": random.randint(5, 15),
                        "unit": "cm",
                        "description": "Dimensions of the box",
                        "timestamp": now.isoformat(),
                    },
                    "sealingMethod": {
                        "value": "Glue",
                        "unit": "method",
                        "description": "Method used for sealing the box",
                        "timestamp": now.isoformat(),
                    },
                    "conveyorSpeed": {
                        "value": random.randint(10, 100),
                        "unit": "cm/s",
                        "description": "Current speed of the conveyor belt",
                        "timestamp": now.isoformat(),
                    },
                    "speedOffset": {
                        "value": random.randint(1, 5),
                        "unit": "cm/s",
                        "description": "Offset parameter to sync wrapping and boxing machine",
                        "timestamp": now.isoformat(),
                    },
                    "timestamp": now.isoformat(),
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "ComponentFailure",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "SPM001",
                }
            },
            "PLM001": {
                "informations": {
                    "type": "LabelingMachine",
                    "manufacturer": "LabelTech",
                    "modelYear": str(random.randint(2015, 2021)),
                    "serialNumber": f"LM{random_string(5)}",
                    "capacity": random.randint(1000, 1500),
                    "capacityUnit": "pcs/hour",
                    "ratedPower": "2000 WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "LM001",
                },
                "machineData": {
                    "labelType": {
                        "value": "Print",
                        "unit": "material",
                        "description": "Type of label used",
                        "timestamp": now.isoformat(),
                    },
                    "labelDimensions": {
                        "length": random.randint(5, 15),
                        "width": random.randint(5, 10),
                        "unit": "cm",
                        "description": "Dimensions of the label",
                        "timestamp": now.isoformat(),
                    },
                    "printingMethod": {
                        "value": "Inkjet",
                        "unit": "method",
                        "description": "Method used for printing the label",
                        "timestamp": now.isoformat(),
                    },
                    "expiryDate": {
                        "value": "31.10.2025",
                        "description": "Expiry date set for current batch. Format YYYY.MM.DD",
                        "timestamp": now.isoformat(),
                    },
                    "batchNumber": {
                        "value": random_string(10),
                        "description": "Batch for print on pizza box",
                        "timestamp": now.isoformat(),
                    },
                    "labelContent": {
                        "value": f"{(now + timedelta(days=1)).strftime('%Y.%m.%d')}\n{random_string(10)}",
                        "description": "Combined label content for print on pizza box ",
                        "timestamp": now.isoformat(),
                    },
                    "timestamp": now.isoformat(),
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "LabelJam",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "LM001",
                }
            },
            "PPM001": {
                "informations": {
                    "type": "PalletPackagingMachine",
                    "manufacturer": "PalletTech",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"PPM{random_string(5)}",
                    "capacity": random.randint(1500, 2500),
                    "capacityUnit": "items/hour",
                    "ratedPower": "3000 WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "PPM001",
                },
                "machineData": {
                    "palletType": {
                        "value": "Wood",
                        "unit": "material",
                        "description": "Type of pallet used",
                        "timestamp": now.isoformat(),
                    },
                    "palletDimensions": {
                        "length": random.randint(100, 150),
                        "width": random.randint(100, 150),
                        "height": random.randint(10, 20),
                        "unit": "cm",
                        "description": "Dimensions of the pallet",
                        "timestamp": now.isoformat(),
                    },
                    "palletLoad": {
                        "value": random.randint(10, 50),
                        "unit": "items",
                        "description": "Number of items loaded on the pallet",
                        "timestamp": now.isoformat(),
                    },
                    "plannedPalletLoad": {
                        "value": random.randint(40, 60),
                        "unit": "items",
                        "description": "Planned items on pallet",
                        "timestamp": now.isoformat(),
                    },
                    "palletWeight": {
                        "value": random.randint(100, 300),
                        "unit": "kg",
                        "description": "Weight of the items on pallet",
                        "timestamp": now.isoformat(),
                    },
                    "timestamp": now.isoformat(),
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "LoadInstability",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "PPM001",
                }
            }
        }
    }
    return simulated_data

def generate_topping_and_freezing_data():
    now = datetime.now()
    simulated_data = {
        "topping": {
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuantity": random.randint(100, 1000),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": None
            },
            "MES": {
                "Production": {
                "JobStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(0, 1))
                },
                "JobStartTime": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": (now + timedelta(days=1, hours=1)).strftime("%m/%d/%Y %H:%M:%S")
                },
                "JobEndTime": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": (now + timedelta(days=1, hours=4)).strftime("%m/%d/%Y %H:%M:%S")
                },
                "RejectedQuantity": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(0, 10))
                },
                "ProducedQuantity": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(200, 300))
                }
                },
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    }
                },
                "Quality": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "OrderNumber": random.randint(100000, 999999),
                    "AcceptanceQuantity": random.randint(100, 250),
                    "RejectionQuantity": random.randint(0, 50),
                    "TestingParameters": random_string(14)
                },
                "MaintenanceStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": random.randint(0, 1)
                }
            },
            "CMMS": {
                "maintenanceJobList": [
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "machineId": "PWR001",
                        "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                        "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                        "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                        "maintenanceType": random.choice(["preventive", "corrective"]),
                        "maintenanceTechnician": random.choice([None, random_string(5)]),
                    }
                ]              
            },
            "RCA004": {
            "informations": {
                "type": "RoomClimateAnalyzer",
                "manufacturer": "AirMasters",
                "modelYear": str(random.randint(2015, 2022)),
                "serialNumber": f"RCA{random_string(5)}",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "RCA004",
                
            },
            "machineData": {
                "ambiantHumidity": {
                    "value": random.randint(70, 90),
                    "unit": "%"
                },
                "ambiantTemperature": {
                    "value": random.randint(10, 18),
                    "unit": "°C"
                }
            }
        },
            "TSD001": {
                "informations": {
                "type": "TomatoSauceDispenser",
                "manufacturer": "TomatoTech",
                "modelYear": str(random.randint(2018, 2022)),
                "serialNumber": f"TS{random_string(5)}",
                "capacity": random.randint(10, 30),
                "capacityUnit": "L/hour",
                "ratedPower": f"{random.randint(2000, 3000)} WATTS",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "TSD001"
                },
                "machineData": {
                    "sauceAmount": {
                        "value": random.randint(100, 200),
                        "unit": "g",
                        "description": "Amount of tomato sauce applied",
                        "timestamp": now.isoformat()
                    },
                    "applicationTime": {
                        "value": random.randint(3, 7),
                        "unit": "seconds",
                        "timestamp": now.isoformat()
                    },
                    "temperature": {
                        "value": random.randint(20, 25),
                        "unit": "°C",
                        "description": "Temperature of the tomato sauce",
                        "timestamp": now.isoformat()
                    },
                    "spreadMethod": {
                        "value": random.choice(["Rotary spreader", "Nozzle sprayer"]),
                        "timestamp": now.isoformat()
                    }
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "HumanControlNeeded",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "TSD001"
                }
            },
            "CHD001": {
                "informations": {
                "type": "CheeseDispenser",
                "manufacturer": "DairyTech",
                "modelYear": str(random.randint(2015, 2021)),
                "serialNumber": f"C1J{random_string(5)}",
                "capacity": random.randint(5, 15),
                "capacityUnit": "kg/hour",
                "ratedPower": f"{random.randint(2500, 3500)} WATTS",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "CHD001"
                },
                "machineData": {
                    "cheeseAmount": {
                    "value": random.randint(50, 150),
                    "unit": "g",
                    "description": "Amount of shredded cheese applied",
                    "timestamp": now.isoformat()
                    },
                    "applicationTime": {
                        "value": random.randint(2, 5),
                        "unit": "seconds",
                        "timestamp": now.isoformat()
                    },
                    "distributionMethod": {
                        "value": random.choice(["Automatic dispenser", "Manual spreader"]),
                        "timestamp": now.isoformat()
                    },
                    "temperature": {
                        "value": random.randint(0, 8),
                        "unit": "°C",
                        "description": "Temperature of the cheese",
                        "timestamp": now.isoformat()
                    }
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "ComponentFailure",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "CD001"
                }
            },
            "MSPM001": {
                "informations": {
                "type": "MozzarellaSlicingPlacingMachine",
                "manufacturer": "DairyTech",
                "modelYear": str(random.randint(2018, 2023)),
                "serialNumber": f"MZ{random_string(5)}",
                "capacity": random.randint(30, 70),
                "capacityUnit": "kg/hour",
                "ratedPower": f"{random.randint(3000, 5000)} WATTS",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "MSPM001"
                },
                "machineData": {
                    "mozzSlizes": {
                        "value": random.randint(5, 15),
                        "unit": "slices",
                        "description": "Number of mozzarella slices added",
                        "timestamp": now.isoformat()
                    },
                    "sliceThickness": {
                        "value": round(random.uniform(0.3, 0.7), 2),
                        "unit": "cm",
                        "description": "Thickness of each mozzarella slice",
                        "timestamp": now.isoformat()
                    },
                    "placementPattern": {
                        "value": random.choice(["Evenly distributed", "Randomly distributed"]),
                        "timestamp": now.isoformat()
                    }
                },
                "alarms": {
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "alarmId": random.randint(10000, 99999),
                "alarmType": "ComponentFailure",
                "alarmStatus": random.choice(["Cleared", "Active"]),
                "machineId": "MSPM001"
                }
            },
            "CTPM001": {
                "informations": {
                "type": "CherryTomatoPlacingMachine",
                "manufacturer": "VeggieTech",
                "modelYear": str(random.randint(2018, 2023)),
                "serialNumber": f"CTP{random_string(5)}",
                "capacity": random.randint(20, 40),
                "capacityUnit": "kg/hour",
                "ratedPower": f"{random.randint(3000, 4000)} WATTS",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "CTPM001"
                },
                "machineData": {
                    "tomatoNumbers": {
                        "value": random.randint(5, 15),
                        "unit": "pcs",
                        "description": "Number of cherry tomatoes added",
                        "timestamp": now.isoformat()
                    },
                    "cutStyle": {
                        "value": random.choice(["Halved", "Quartered"]),
                        "timestamp": now.isoformat()
                    },
                    "placementPattern": {
                        "value": random.choice(["Evenly distributed", "Randomly distributed"]),
                        "timestamp": now.isoformat()
                    }
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "ComponentFailure",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "CTPM001"
                }
            },
            "HSP001": {
                "informations": {
                "type": "HerbSprinkler",
                "manufacturer": "HerbTech",
                "modelYear": str(random.randint(2018, 2023)),
                "serialNumber": f"HS{random_string(5)}",
                "capacity": random.randint(10, 20),
                "capacityUnit": "kg/hour",
                "ratedPower": f"{random.randint(1000, 2000)} WATTS",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "HS001"
                },
                "machineData": {
                    "herbWeight": {
                        "value": random.randint(3, 7),
                        "unit": "g",
                        "description": "Amount of herbs applied",
                        "timestamp": now.isoformat()
                    },
                "herbType": {
                    "value": random.choice(["Mixed Italian herbs", "Basil", "Oregano"]),
                    "timestamp": now.isoformat()
                },
                "applicationMethod": {
                    "value": random.choice(["Sprinkled manually", "Sprinkled automatically"]),
                    "timestamp": now.isoformat()
                },
                "origin": {
                    "value": random.choice(["Organic", "Non-Organic"]),
                    "timestamp": now.isoformat()
                },
                
                },
                "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "ComponentFailure",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "HS001"
                }
            }
        },
        "freezing": {
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuantity": random.randint(100, 1000),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": None
            },
            "MES": {
                "Production": {
                "JobStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(0, 1))
                },
                "JobStartTime": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": (now + timedelta(days=1, hours=1)).strftime("%m/%d/%Y %H:%M:%S")
                },
                "JobEndTime": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": (now + timedelta(days=1, hours=4)).strftime("%m/%d/%Y %H:%M:%S")
                },
                "RejectedQuantity": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(0, 10))
                },
                "ProducedQuantity": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": str(random.randint(200, 300))
                }
                },
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    }
                },
                "Quality": {
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "OrderNumber": random.randint(100000, 999999),
                "AcceptanceQuantity": random.randint(100, 250),
                "RejectionQuantity": random.randint(0, 50),
                "TestingParameters": random_string(14)
                },
                "MaintenanceStatus": {
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "value": random.randint(0, 1)
                }
            },
            "CMMS": {
                "maintenanceJobList": [
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "machineId": "PWR001",
                        "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                        "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                        "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                        "maintenanceType": random.choice(["preventive", "corrective"]),
                        "maintenanceTechnician": random.choice([None, random_string(5)]),
                    }
                ]              
            },
            "RCA005": {
            "informations": {
                "type": "RoomClimateAnalyzer",
                "manufacturer": "AirMasters",
                "modelYear": str(random.randint(2015, 2022)),
                "serialNumber": f"RCA{random_string(5)}",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "RCA005",
                
            },
            "machineData": {
                "ambiantHumidity": {
                    "value": random.randint(70, 90),
                    "unit": "%"
                },
                "ambiantTemperature": {
                    "value": random.randint(10, 18),
                    "unit": "°C"
                }
            }
        },
            "BF001": {
                  "informations": {
                    "type": "BlastFreezer",
                    "manufacturer": "FreezeTech",
                    "modelYear": str(random.randint(2018, 2023)),
                    "serialNumber": f"BF{random_string(5)}",
                    "capacity": random.randint(400, 600),
                    "capacityUnit": "kg/hour",
                    "ratedPower": f"{random.randint(4000, 6000)} WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "BF001"
                  },
                  "machineData": {
                    "temperature": {
                      "value": random.randint(-35, -25),
                      "unit": "°C",
                      "description": "Freezing temperature",
                      "timestamp": now.isoformat()
                    },
                    "consistencyCheckInterval": {
                      "value": random.randint(20, 40),
                      "unit": "minutes",
                      "description": "Interval in which the temperature is checked for consistency",
                      "timestamp": now.isoformat()
                    },
                    "freezingTime": {
                      "value": random.randint(10, 20),
                      "unit": "minutes",
                      "description": "Total time for the pizza to be fully frozen",
                      "timestamp": now.isoformat()
                    },
                    "coolingRate": {
                      "value": random.uniform(1.5, 2.5),
                      "unit": "°C/minute",
                      "description": "Rate at which the pizza cools in the freezer",
                      "timestamp": now.isoformat()
                    },
                    "freezingMethod": {
                      "value": "Blast freezer",
                      "timestamp": now.isoformat()
                    }
                  },
                  "alarms": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "alarmId": random.randint(10000, 99999),
                    "alarmType": "TemperatureDeviation",
                    "alarmStatus": random.choice(["Cleared", "Active"]),
                    "machineId": "BF001"
                  }
                }
        }
    }
    return simulated_data

def generate_dough_prep_data():
    now = datetime.now()
    simulated_data = {
        "pizzaDoughPreparation": {
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuanity": random.randint(100, 1000),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": random.choice([None, "Vegetarian", "Non-Vegetarian", "Vegan"]),
            },
            "MES": {
                "production": [
                    {
                        "machine_id": f"DKM{str(i).zfill(3)}",
                        "jobStatus": {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "value": str(random.randint(0, 1)),
                        },
                        "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "jobEndTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "producedQuantity": {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "value": str(random.randint(0, 200)),
                        },
                        "recipe": {
                            "flourWeight": {"value": random.randint(200, 500), "unit": "kg"},
                            "waterWeight": {"value": random.randint(100, 300), "unit": "kg"},
                            "yeastWeight": {"value": random.randint(5, 20), "unit": "kg"},
                            "saltWeight": {"value": random.randint(5, 15), "unit": "kg"},
                            "oilWeight": {"value": random.randint(5, 15), "unit": "kg"},
                        },
                        "qualityParameters": {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "OrderNumber": random.randint(100000, 999999),
                            "doughTemperatureMin": {"value": str(random.randint(9, 13)), "unit": "°C"},
                            "doughTemperatureMax": {"value": str(random.randint(14, 18)), "unit": "°C"},
                            "ambiantHumidityMin": {"value": str(random.randint(70, 75)), "unit": "%"},
                            "ambiantHumidityMax": {"value": str(random.randint(80, 90)), "unit": "%"},
                            "ambiantTemperatureMin": {"value": str(random.randint(10, 13)), "unit": "°C"},
                            "ambiantTemperatureMax": {"value": str(random.randint(14, 18)), "unit": "°C"},
                        }
                    }
                    for i in range(1, 4)
                ],
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    }
                }
            },
            "CMMS": {
                    "maintenanceJobList": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "machineId": "PWR001",
                            "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                            "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                            "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                            "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                            "maintenanceType": random.choice(["preventive", "corrective"]),
                            "maintenanceTechnician": random.choice([None, random_string(5)]),
                        }
                    ]              
                },
            "RCA001": {
                "informations": {
                    "type": "RoomClimateAnalyzer",
                    "manufacturer": "AirMasters",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"RCA{random_string(5)}",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "RCA001",
                },
                "machineData": {
                    "ambiantHumidity": {
                        "value": random.randint(70, 90),
                        "unit": "%"
                    },
                    "ambiantTemperature": {
                        "value": random.randint(10, 18),
                        "unit": "°C"
                    }
                }
            },
            **{
                f"DKM{str(i).zfill(3)}": {
                    "informations": {
                        "type": "DoughKneadingMachine",
                        "manufacturer": "DoughMasters",
                        "modelYear": str(random.randint(2014, 2022)),
                        "serialNumber": f"KM{random_string(5)}",
                        "capacity": random.randint(500, 1500),
                        "capacityUnit": "kg",
                        "ratedPower": random.randint(1000, 2000),
                        "unit": "WATTS",
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "machineId": f"DKM{str(i).zfill(3)}",
                    },
                    "machineData": {
                        "machineStatus": {
                            "value": random.randint(0, 1),
                            "unit": "integer",
                            "description": "Machine status. Running = 1, Stopped = 0",
                            "timestamp": now.isoformat(),
                        },
                        "loadingWeight": {
                            "value": random.randint(1000, 5000),
                            "unit": "g",
                            "description": "Total weight of product in kneading machine",
                            "timestamp": now.isoformat(),
                        },
                        "kneadingTime": {
                            "value": random.randint(1000, 2000),
                            "unit": "seconds",
                            "description": "Total kneading time for the dough",
                            "timestamp": now.isoformat(),
                        },
                        "remainingTime": {
                            "value": random.randint(0, 100),
                            "unit": "seconds",
                            "description": "Remaining Time until kneading is finished",
                            "timestamp": now.isoformat(),
                        },
                        "speed": {
                            "value": random.randint(100, 300),
                            "unit": "rpm",
                            "description": "Current speed of the kneading machine",
                            "timestamp": now.isoformat(),
                        },
                        "doughTemperature": {
                            "value": random.randint(10, 25),
                            "unit": "°C",
                            "description": "Temperature of the dough during kneading",
                            "timestamp": now.isoformat(),
                        },
                        "alarms": [
                            {
                                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                                "alarmId": random.randint(10000, 99999),
                                "alarmType": random.choice(["KneadingTimeExceeded", "DoughTemperatureTooHigh"]),
                                "alarmStatus": random.choice(["Cleared", "Active"]),
                                "machineId": f"DKM{str(i).zfill(3)}"
                            }
                            for _ in range(2)
                        ]
                    }
                } for i in range(1, 4)
            }
    },
        "portioningAndForming": {
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuanity": random.randint(1000, 3000),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": random.choice([None, "Vegetarian", "Non-Vegetarian", "Vegan"]),
            },
            "MES": {
                "production": {
                    "jobStatus": str(random.randint(0, 1)),
                    "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                    "jobEndTime": random_date(now, now + timedelta(days=1)).isoformat(),
                    "producedQuantity": str(random.randint(100, 300)),
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                },
                "quality": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "OrderNumber": random.randint(100000, 999999),
                    "AcceptanceQuantity": random.randint(100, 300),
                    "RejectionQuantity": random.randint(0, 10),
                    "minWeightPerBun": {"value": random.randint(140, 150), "unit": "g"},
                    "maxWeightPerBun": {"value": random.randint(151, 160), "unit": "g"},
                    "minBunsPerMinute": {"value": random.randint(35, 45), "unit": "1/min"},
                    "maxBunsPerMinute": {"value": random.randint(46, 60), "unit": "1/min"},
                    "minBunDiameter": {"value": random.randint(7, 10), "unit": "cm"},
                    "maxBunDiameter": {"value": random.randint(11, 14), "unit": "cm"},
                    "minFormedDiameter": {"value": random.randint(20, 25), "unit": "cm"},
                    "maxFormedDiameter": {"value": random.randint(26, 30), "unit": "cm"},
                },
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    },
                },
                "MaintenanceStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": random.randint(0, 1),
                }
            },
            "CMMS": {
                "maintenanceJobList": [
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "machineId": "PWR001",
                        "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                        "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                        "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                        "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                        "maintenanceType": random.choice(["preventive", "corrective"]),
                        "maintenanceTechnician": random.choice([None, random_string(5)]),
                    }
                ]              
            },
            "RCA003": {
            "informations": {
                "type": "RoomClimateAnalyzer",
                "manufacturer": "AirMasters",
                "modelYear": str(random.randint(2015, 2022)),
                "serialNumber": f"RCA{random_string(5)}",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "RCA003",
                
            },
            "machineData": {
                "ambiantHumidity": {
                    "value": random.randint(70, 90),
                    "unit": "%"
                },
                "ambiantTemperature": {
                    "value": random.randint(10, 18),
                    "unit": "°C"
                }
            }
            },
            "PTN001": {
                "informations": {
                    "type": "Portioner",
                    "manufacturer": "PortionMaster",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"PM{random_string(5)}",
                    "capacity": random.randint(500, 1500),
                    "capacityUnit": "kg",
                    "operatingPressure": random.randint(3, 8),
                    "operatingPressureUnit": "bar",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "PTN001",
                },
                "machineData": {
                    "weightOfBun": {
                        "value": random.randint(80, 120),
                        "unit": "g",
                        "description": "Weight of each portion",
                        "timestamp": now.isoformat(),
                    },
                    "diameterOfBun": {
                        "value": random.randint(5, 15),
                        "unit": "cm",
                        "description": "Size of each portion",
                        "timestamp": now.isoformat(),
                    },
                    "speed": {
                        "value": random.randint(30, 70),
                        "unit": "buns/min",
                        "description": "Portioning speed",
                        "timestamp": now.isoformat(),
                    },
                    "alarms": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": random.choice(["PortionSizeMismatch", "PortionWeightMismatch"]),
                            "alarmStatus": random.choice(["Active", "Resolved"]),
                            "machineId": "PTN001"
                        }
                        for _ in range(2)
                    ]
                }
            },
            "FRM001": {
                "informations": {
                    "type": "Former",
                    "manufacturer": "FormMaster",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"FM{random_string(5)}",
                    "capacity": random.randint(50, 100),
                    "capacityUnit": "forms/minute",
                    "ratedPower": random.randint(5000, 7000),
                    "unit": "WATTS",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "FRM001",
                },
                "machineData": {
                    "formingTime": {
                        "value": random.randint(1, 5),
                        "unit": "s",
                        "description": "Time to form one portion",
                        "timestamp": now.isoformat(),
                    },
                    "pressure": {
                        "value": random.randint(3, 7),
                        "unit": "bar",
                        "description": "Forming pressure",
                        "timestamp": now.isoformat(),
                    },
                    "formedDiameter": {
                        "value": random.randint(20, 30),
                        "unit": "cm",
                        "description": "Forming diameter",
                        "timestamp": now.isoformat(),
                    },
                    "alarms": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": random.choice(["pressureDrop", "formedSizeMismatch"]),
                            "alarmStatus": random.choice(["Cleared", "Active"]),
                            "machineId": "FRM001",
                        },
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": "formedSizeMismatch",
                            "alarmStatus": "Cleared",
                            "machineId": "PTN001",
                        }
                    ]
                }
            },
            "BLT001": {
                "informations": {
                    "type": "ConveyorBelt",
                    "manufacturer": "ConveyorMasters",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"CB{random_string(5)}",
                    "capacity": random.randint(50, 150),
                    "capacityUnit": "kg/m",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "BLT001",
                },
                "machineData": {
                    "beltSpeed": {
                        "value": round(random.uniform(0.1, 1.0), 2),
                        "unit": "m/s",
                        "description": "Speed of the conveyor belt",
                        "timestamp": now.isoformat(),
                    },
                    "temperature": {
                        "value": random.randint(0, 25),
                        "unit": "°C",
                        "description": "Temperature around the conveyor belt",
                        "timestamp": now.isoformat(),
                    },
                    "alarms": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": "BeltStopped",
                            "alarmStatus": "Active",
                            "machineId": "CVB001"
                        }
                    ]
                }
            }
    },
        "bakingAndCooldown": {
            "ERP": {
                "OrderNumber": random.randint(100000, 999999),
                "OrderQuanity": random.randint(100, 300),
                "PriorityLevel": random.choice(["High", "Medium", "Low"]),
                "ScheduledStartDate": (now + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
                "ScheduledEndDate": (now + timedelta(days=1, hours=3)).strftime("%m/%d/%Y %H:%M:%S"),
                "BatchNumber": f"Batch-{random_string(5)}",
                "ProductInformation": random.choice([None, "Vegetarian", "Non-Vegetarian", "Vegan"]),
            },
            "MES": {
                "production": {
                    "jobStatus": str(random.randint(0, 1)),
                    "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                    "jobEndTime": random_date(now, now + timedelta(days=1)).isoformat(),
                    "producedQuantity": str(random.randint(1, 200)),
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                },
                "quality": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "OrderNumber": random.randint(100000, 999999),
                    "AcceptanceQuantity": random.randint(100, 200),
                    "RejectionQuantity": random.randint(0, 10),
                    "minOvenTemperature": {
                        "value": random.randint(210, 215),
                        "unit": "°C"
                    },
                    "maxOvenTemperature": {
                        "value": random.randint(220, 225),
                        "unit": "°C"
                    },
                    "minTempAfterCooldown": {
                        "value": random.randint(15, 18),
                        "unit": "°C"
                    },
                    "maxTempAfterCooldown": {
                        "value": random.randint(20, 25),
                        "unit": "°C"
                    }
                },
                "KPI": {
                    "OEE": generate_oee(),
                    "MTTR": {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "value": str(random.uniform(10, 100))
                    }
                },
                "MaintenanceStatus": {
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "value": random.randint(0, 1),
                }
            },
            "CMMS": {
                    "maintenanceJobList": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "machineId": "PWR001",
                            "jobStatus": random.choice(["scheduled", "ongoing", "completed"]),
                            "jobStartTime": random_date(now, now + timedelta(days=1)).isoformat(),
                            "jobEndTime": random_date(now, now + timedelta(days=1, hours=1)).isoformat(),
                            "jobDescription": random.choice(["conveyor belt maintenance", "routine check"]),
                            "maintenanceType": random.choice(["preventive", "corrective"]),
                            "maintenanceTechnician": random.choice([None, random_string(5)]),
                        }
                    ]              
                },
            "RCA002": {
                "informations": {
                    "type": "RoomClimateAnalyzer",
                    "manufacturer": "AirMasters",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"RCA{random_string(5)}",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "RCA002",

                },
                "machineData": {
                    "ambiantHumidity": {
                        "value": random.randint(70, 90),
                        "unit": "%"
                    },
                    "ambiantTemperature": {
                        "value": random.randint(10, 18),
                        "unit": "°C"
                    }
                }
            },
            "OVN001": {
                "informations": {
                    "type": "Oven",
                    "manufacturer": "BakeMaster",
                    "modelYear": str(random.randint(2015, 2022)),
                    "serialNumber": f"OV{random_string(5)}",
                    "capacity": random.randint(50, 150),
                    "capacityUnit": "pizzas/min",
                    "standardOperatingTemperature": random.randint(210, 230),
                    "temperatureUnit": "°C",
                    "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                    "machineId": "OVN001"
                },
                "machineData": {
                    "bakingTime": {
                        "value": random.randint(10, 15),
                        "unit": "minutes",
                        "description": "Total baking time for each pizza",
                        "timestamp": now.isoformat()
                    },
                    "entranceOvenTemperature": {
                        "value": random.randint(210, 220),
                        "unit": "°C",
                        "description": "Oven temperature entrance measurement",
                        "timestamp": now.isoformat()
                    },
                    "centerOvenTemperature": {
                        "value": random.randint(220, 230),
                        "unit": "°C",
                        "description": "Oven temperature center measurement",
                        "timestamp": now.isoformat()
                    },
                    "exitOvenTemperature": {
                        "value": random.randint(215, 225),
                        "unit": "°C",
                        "description": "Oven temperature exit measurement",
                        "timestamp": now.isoformat()
                    },
                    "alarms": [
                        {
                            "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                            "alarmId": random.randint(10000, 99999),
                            "alarmType": "entranceTemperatureTooLow",
                            "alarmStatus": "Active",
                            "machineId": "OVN001"
                        }
                    ]
                }
            },
            "BLT002": {
            "informations": {
                "type": "ConveyorBelt",
                "manufacturer": "ConveyorMasters",
                "modelYear": str(random.randint(2015, 2022)),
                "serialNumber": f"CB{random_string(5)}",
                "capacity": random.randint(50, 150),
                "capacityUnit": "kg/m",
                "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                "machineId": "BLT002"
            },
            "machineData": {
                "beltSpeed": {
                    "value": round(random.uniform(0.1, 1.0), 2),
                    "unit": "m/s",
                    "description": "Speed of the conveyor belt",
                    "timestamp": now.isoformat()
                },
                "pizzaExitTemperature": {
                    "value": random.randint(15, 25),
                    "unit": "°C",
                    "description": "Temperature of pizzas after cooldown",
                    "timestamp": now.isoformat()
                },
                "alarms": [
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "alarmId": random.randint(10000, 99999),
                        "alarmType": "BeltSpeedTooLow",
                        "alarmStatus": "Cleared",
                        "machineId": "CVB002"
                    },
                    {
                        "timestamp": random_date(now, now + timedelta(days=1)).isoformat(),
                        "alarmId": random.randint(10000, 99999),
                        "alarmType": "exitTemperatureExceeded",
                        "alarmStatus": "Cleared",
                        "machineId": "CVB002"
                    }
                ]
            }
        }
    }
    }    
    return simulated_data