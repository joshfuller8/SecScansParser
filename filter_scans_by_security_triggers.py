# from datetime import datetime


def create_list_of_filtered_scans(validated_scans_by_cn, customer_nums_to_ignore, triggers, trigger_parameters):

    filtered_rows_that_meet_criteria = []

    # Process customer rows and filter based on criteria and place in filtered_rows
    # run_filtered_rows = True
    for customer_number, scans in validated_scans_by_cn.items():
        for i in range(len(scans)):
            for j in range(i + 1, len(scans)):
                # validate date field again just because
                if scans[i][1] is None or scans[j][1] is None:
                    continue

                # remove certain CN#s from results, test badges, staff, things like that
                if customer_number in customer_nums_to_ignore:
                    continue

                # define variables to make the appends less confusing

                # variables for i
                time_i = scans[i][1]
                tablet_i = scans[i][2]
                loc_i = scans[i][3]

                # variables for j
                time_j = scans[j][1]
                tablet_j = scans[j][2]  # specifically the last 4 digits of asset tag on back of tablet
                loc_j = scans[j][3]  # physical location of the tablet, ie. front doors, garage etc....

                # define the time difference between the two referenced scans
                time_diff = abs(time_j - time_i).total_seconds()

                # conditions that trigger scan data to be added to filtered rows
                if triggers['same_tablet_within_range']:
                    if tablet_i == tablet_j and trigger_parameters['SAME_TABLET_LOWER'] <= time_diff <= \
                            trigger_parameters['SAME_TABLET_UPPER']:
                        filtered_rows_that_meet_criteria.append([customer_number, time_i, tablet_i, loc_i])
                        filtered_rows_that_meet_criteria.append([customer_number, time_j, tablet_j, loc_j])
                if triggers['diff_tablet_under_5_mins'] and tablet_i != tablet_j and time_diff <= \
                        trigger_parameters['DIFF_TABLET_UPPER']:
                    filtered_rows_that_meet_criteria.append([customer_number, time_i, tablet_i, loc_i])
                    filtered_rows_that_meet_criteria.append([customer_number, time_j, tablet_j, loc_j])

                # print statement for debugging
                # if len(filtered_rows) > 10 and run_filtered_rows:
                #     print('filtered_rows')
                #     print(filtered_rows)
                #     run_filtered_rows = False
    # print(filtered_rows_that_meet_criteria)
    return filtered_rows_that_meet_criteria
