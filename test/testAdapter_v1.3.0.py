



if __name__ == '__main__':
    test = Test()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(test.setup_digitaltwins("ep1"))
    loop.run_until_complete(test.test_generate_report(patient_uuid="54f2abff-6594-11ef-917d-484d7e9beb16",
                                                      workflow_uuid="e3b3eaa0-65ae-11ef-917d-484d7e9beb16",
                                                      workflow_tool_uuid="b6b7b363-65ae-11ef-917d-484d7e9beb16",
                                                      dataset_uuid="93d49efa-5f4e-11ef-917d-484d7e9beb16"))