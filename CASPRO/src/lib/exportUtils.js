// src/lib/exportUtils.js
// Utility helper to export auction sales & team rosters as JSON or CSV format

/**
 * Helper to download a string of data as a file in the browser
 */
function downloadFile(content, fileName, contentType) {
  const blob = new Blob([content], { type: contentType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/**
 * Format lakhs to display string (e.g. 150 -> "1.50 Cr", 50 -> "50 Lakhs")
 */
function formatLakhs(lakhs) {
  if (lakhs == null || isNaN(lakhs)) return '0 Lakhs';
  if (lakhs >= 100) return `${(lakhs / 100).toFixed(2)} Cr`;
  return `${lakhs} Lakhs`;
}

/**
 * Export full auction roster data per team in JSON format
 * Creates an object indexed by Team Name / ID with squad details and purse stats.
 */
export function exportRostersJSON(teams, playerSales = {}) {
  const exportData = {
    exportDate: new Date().toISOString(),
    system: "CASPRO Mock IPL Auction System",
    teams: teams.map(t => {
      const squad = (t.squad || []).map(p => ({
        id: p.id,
        name: p.name,
        role: p.role,
        isOverseas: !!p.is_overseas,
        isRookie: !!p.is_rookie,
        rating: p.rating || null,
        basePriceLakhs: p.base_price_lakhs,
        basePriceFormatted: formatLakhs(p.base_price_lakhs),
        soldPriceLakhs: p.sold_price_lakhs,
        soldPriceFormatted: formatLakhs(p.sold_price_lakhs),
      }));

      return {
        teamId: t.id,
        teamName: t.name,
        shortName: t.shortName,
        purseInitialLakhs: t.initialPurseLakhs || 12000,
        purseRemainingLakhs: t.purseLakhs,
        purseSpentLakhs: (t.initialPurseLakhs || 12000) - t.purseLakhs,
        purseRemainingFormatted: formatLakhs(t.purseLakhs),
        purseSpentFormatted: formatLakhs((t.initialPurseLakhs || 12000) - t.purseLakhs),
        totalPlayers: squad.length,
        overseasPlayers: squad.filter(p => p.isOverseas).length,
        squad: squad,
      };
    })
  };

  const jsonStr = JSON.stringify(exportData, null, 2);
  const fileName = `IPL_Auction_Team_Rosters_${new Date().toISOString().slice(0, 10)}.json`;
  downloadFile(jsonStr, fileName, 'application/json');
}

/**
 * Export full auction roster data as CSV format
 * Generates a clean tabular CSV sheet readable by Microsoft Excel, Google Sheets, etc.
 */
export function exportRostersCSV(teams) {
  const headers = [
    'Team ID',
    'Team Name',
    'Player ID',
    'Player Name',
    'Role',
    'Overseas',
    'Rookie',
    'Rating',
    'Base Price (Lakhs)',
    'Sold Price (Lakhs)',
    'Sold Price (Formatted)',
    'Team Remaining Purse (Lakhs)',
  ];

  const rows = [];

  teams.forEach(t => {
    const squad = t.squad || [];
    if (squad.length === 0) {
      // Add entry even if team bought 0 players
      rows.push([
        `"${t.id}"`,
        `"${t.name}"`,
        '""',
        '"No Players Bought"',
        '""',
        '""',
        '""',
        '""',
        '""',
        '""',
        '""',
        t.purseLakhs,
      ]);
    } else {
      squad.forEach(p => {
        rows.push([
          `"${t.id}"`,
          `"${t.name}"`,
          `"${p.id}"`,
          `"${p.name.replace(/"/g, '""')}"`,
          `"${p.role || ''}"`,
          p.is_overseas ? 'Yes' : 'No',
          p.is_rookie ? 'Yes' : 'No',
          p.rating ?? '',
          p.base_price_lakhs ?? '',
          p.sold_price_lakhs ?? '',
          `"${formatLakhs(p.sold_price_lakhs)}"`,
          t.purseLakhs,
        ]);
      });
    }
  });

  const csvContent = [
    headers.join(','),
    ...rows.map(r => r.join(','))
  ].join('\n');

  const fileName = `IPL_Auction_Team_Rosters_${new Date().toISOString().slice(0, 10)}.csv`;
  downloadFile(csvContent, fileName, 'text/csv;charset=utf-8;');
}
