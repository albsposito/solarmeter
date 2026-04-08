SELECT
  'solarmeter' AS inverter_id,
  get(get(*, 0), 'time') AS time,
  get(get(*, 0), 'total_energy') AS total_energy,
  get(get(*, 0), 'grid_power') AS grid_power,
  get(get(*, 0), 'grid_voltage') AS grid_voltage,
  get(get(*, 0), 'inverter_temp') AS inverter_temp,
  get(get(*, 0), 'efficiency') AS efficiency
FROM 'solarmeter/#'
