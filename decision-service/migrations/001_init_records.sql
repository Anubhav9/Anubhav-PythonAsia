CREATE TABLE IF NOT EXISTS records (
    application_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    id_number TEXT NOT NULL,
    dob DATE NOT NULL,
    loan_type TEXT NOT NULL,
    loan_tenure INTEGER NOT NULL,
    loan_amount NUMERIC(14, 2) NOT NULL,
    result TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_records_result ON records(result);
