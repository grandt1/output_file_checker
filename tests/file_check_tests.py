original = R"Y:\hmds_workspace\tgrand\qc_update2\compare_test_original"
true_copy = R"Y:\hmds_workspace\tgrand\qc_update2\compare_test_true_copy"
altered_file = R"Y:\hmds_workspace\tgrand\qc_update2\compare_test_altered_file"
deleted_file = R"Y:\hmds_workspace\tgrand\qc_update2\compare_test_deleted_file"

tests = [
            [original, true_copy],
            [original, altered_file],
            [original, deleted_file]
    ]