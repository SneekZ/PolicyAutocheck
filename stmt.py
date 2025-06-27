STMT_GET_CLIENTS = """
-- Пациенты, которые обслуживались за последнюю неделю
WITH maxDate AS(
SELECT
  MAX(e.id) AS id,
  MAX(e.createDatetime) AS Date,
  e.client_id
FROM
  Event e
WHERE
  e.deleted = 0
  AND e.createDatetime BETWEEN (CURDATE() - INTERVAL 7 DAY) AND CURDATE()
GROUP BY
  e.client_id
)
-- main
SELECT
  c.id, c.lastName, c.firstName, c.patrName, c.birthDate, rdt.code, CONCAT(cd.serial, ":", cd.number)
FROM
  Client c
LEFT JOIN ClientPolicy cp ON
  c.id = cp.client_id
  AND cp.deleted = 0
  AND cp.endDate >CURRENT_DATE()
  AND cp.begDate <= CURRENT_DATE()
  AND cp.policyKind_id IS NOT NULL
  AND cp.policyType_id IS NOT NULL
INNER JOIN ClientDocument cd ON
  -- Серия и номер документа, удостоверяющего личность
  c.id = cd.client_id
  AND cd.deleted = 0
  AND cd.serial != ''
  AND cd.number != ''
INNER JOIN rbDocumentType rdt ON
  -- Тип документа,
  cd.documentType_id = rdt.id
  AND rdt.EGIZ_code IS NOT NULL
INNER JOIN maxDate md ON
  c.id = md.client_id
WHERE
  c.deleted = 0
  -- Фамилия пациента
  AND c.lastName != ''
  -- Имя пациента
  AND c.firstName != ''
  -- Дата рождения пациента
  AND c.birthDate != '1900-01-01'
  AND c.SNILS != ''
  AND c.notes not regexp 'тест'
  AND cp.id IS NULL;
"""

STMT_GET_LPU_ID = "SELECT netrica_Code FROM OrgStructure WHERE parent_id IS NULL AND deleted = 0"

STMT_INSERT_POLICY_CHECK = "INSERT INTO CheckPolicy (message_id, client_id, date, deleted, requestType, errors) values (%s, %s, CURRENT_DATE(), 0, 1, %s)"