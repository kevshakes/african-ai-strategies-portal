/**
 * African AI Strategies Portal - Main JavaScript
 * Handles interactive features and visualizations
 */

// Global variables
let currentData = {};
let visualizations = {};

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Load initial data
    loadInitialData();
    
    console.log('African AI Strategies Portal initialized');
}

function setupEventListeners() {
    // Country card clicks
    document.querySelectorAll('.country-card').forEach(card => {
        card.addEventListener('click', function() {
            const countryCode = this.dataset.country;
            if (countryCode) {
                window.location.href = `/country/${countryCode}`;
            }
        });
    });
    
    // Search functionality
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
    
    // Comparison functionality
    const compareButton = document.getElementById('compare-button');
    if (compareButton) {
        compareButton.addEventListener('click', handleComparison);
    }
    
    // Export functionality
    const exportButton = document.getElementById('export-button');
    if (exportButton) {
        exportButton.addEventListener('click', handleExport);
    }
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

async function loadInitialData() {
    try {
        showLoading();
        
        // Load countries data
        const countriesResponse = await fetch('/api/countries');
        currentData.countries = await countriesResponse.json();
        
        // Load themes data
        const themesResponse = await fetch('/api/themes');
        currentData.themes = await themesResponse.json();
        
        hideLoading();
        
    } catch (error) {
        console.error('Error loading initial data:', error);
        showError('Failed to load initial data');
    }
}

// Visualization Functions
function createMindMap(containerId, data) {
    const container = d3.select(`#${containerId}`);
    const width = container.node().getBoundingClientRect().width;
    const height = 600;
    
    // Clear existing content
    container.selectAll('*').remove();
    
    const svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const g = svg.append('g')
        .attr('transform', `translate(${width/2},${height/2})`);
    
    // Create tree layout
    const tree = d3.tree()
        .size([2 * Math.PI, Math.min(width, height) / 2 - 100])
        .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);
    
    const root = d3.hierarchy(data);
    tree(root);
    
    // Add links
    g.selectAll('.link')
        .data(root.links())
        .enter().append('path')
        .attr('class', 'mind-map-link')
        .attr('d', d3.linkRadial()
            .angle(d => d.x)
            .radius(d => d.y));
    
    // Add nodes
    const node = g.selectAll('.node')
        .data(root.descendants())
        .enter().append('g')
        .attr('class', 'mind-map-node')
        .attr('transform', d => `
            rotate(${d.x * 180 / Math.PI - 90})
            translate(${d.y},0)
        `);
    
    node.append('circle')
        .attr('r', d => d.data.size || 5)
        .attr('fill', d => getNodeColor(d.data.type));
    
    node.append('text')
        .attr('class', 'mind-map-text')
        .attr('dy', '0.31em')
        .attr('x', d => d.x < Math.PI === !d.children ? 6 : -6)
        .attr('text-anchor', d => d.x < Math.PI === !d.children ? 'start' : 'end')
        .attr('transform', d => d.x >= Math.PI ? 'rotate(180)' : null)
        .text(d => d.data.name)
        .on('mouseover', showTooltip)
        .on('mouseout', hideTooltip);
    
    // Store visualization reference
    visualizations[containerId] = { svg, data };
}

function createNetworkGraph(containerId, data) {
    const container = d3.select(`#${containerId}`);
    const width = container.node().getBoundingClientRect().width;
    const height = 700;
    
    // Clear existing content
    container.selectAll('*').remove();
    
    const svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);
    
    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes)
        .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2));
    
    // Add links
    const link = svg.append('g')
        .selectAll('line')
        .data(data.links)
        .enter().append('line')
        .attr('class', 'network-link')
        .attr('stroke-width', d => Math.sqrt(d.value));
    
    // Add nodes
    const node = svg.append('g')
        .selectAll('circle')
        .data(data.nodes)
        .enter().append('circle')
        .attr('class', 'network-node')
        .attr('r', d => d.size || 10)
        .attr('fill', d => d.color || '#69b3a2')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));
    
    // Add labels
    const label = svg.append('g')
        .selectAll('text')
        .data(data.nodes)
        .enter().append('text')
        .attr('class', 'network-text')
        .text(d => d.name)
        .attr('x', 12)
        .attr('y', 3);
    
    // Add tooltips
    node.on('mouseover', function(event, d) {
        showTooltip(event, d);
    }).on('mouseout', hideTooltip);
    
    // Update positions on simulation tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);
        
        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);
        
        label
            .attr('x', d => d.x + 12)
            .attr('y', d => d.y + 3);
    });
    
    // Drag functions
    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
    
    // Store visualization reference
    visualizations[containerId] = { svg, simulation, data };
}

function createTimeline(containerId, data) {
    const container = d3.select(`#${containerId}`);
    const width = container.node().getBoundingClientRect().width;
    const height = 500;
    const margin = {top: 20, right: 30, bottom: 40, left: 50};
    
    // Clear existing content
    container.selectAll('*').remove();
    
    const svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    
    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Parse dates
    const parseDate = d3.timeParse('%Y-%m-%d');
    data.events.forEach(d => {
        d.date = parseDate(d.date);
    });
    
    // Create scales
    const xScale = d3.scaleTime()
        .domain(d3.extent(data.events, d => d.date))
        .range([0, chartWidth]);
    
    const yScale = d3.scaleBand()
        .domain(data.events.map(d => d.country))
        .range([0, chartHeight])
        .padding(0.1);
    
    // Add axes
    g.append('g')
        .attr('transform', `translate(0,${chartHeight})`)
        .call(d3.axisBottom(xScale));
    
    g.append('g')
        .call(d3.axisLeft(yScale));
    
    // Add events
    g.selectAll('.timeline-event')
        .data(data.events)
        .enter().append('circle')
        .attr('class', 'timeline-event')
        .attr('cx', d => xScale(d.date))
        .attr('cy', d => yScale(d.country) + yScale.bandwidth() / 2)
        .attr('r', 6)
        .attr('fill', d => d.color || '#69b3a2')
        .on('mouseover', showTooltip)
        .on('mouseout', hideTooltip);
    
    // Store visualization reference
    visualizations[containerId] = { svg, data };
}

function createHeatmap(containerId, data) {
    const container = d3.select(`#${containerId}`);
    const width = container.node().getBoundingClientRect().width;
    const height = 400;
    const margin = {top: 50, right: 50, bottom: 100, left: 100};
    
    // Clear existing content
    container.selectAll('*').remove();
    
    const svg = container.append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    
    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Create scales
    const xScale = d3.scaleBand()
        .domain(data.themes)
        .range([0, chartWidth])
        .padding(0.05);
    
    const yScale = d3.scaleBand()
        .domain(data.countries)
        .range([0, chartHeight])
        .padding(0.05);
    
    const colorScale = d3.scaleSequential()
        .interpolator(d3.interpolateBlues)
        .domain([0, 1]);
    
    // Add cells
    g.selectAll('.heatmap-cell')
        .data(data.data)
        .enter().append('rect')
        .attr('class', 'heatmap-cell')
        .attr('x', d => xScale(d.theme))
        .attr('y', d => yScale(d.country))
        .attr('width', xScale.bandwidth())
        .attr('height', yScale.bandwidth())
        .attr('fill', d => colorScale(d.value))
        .on('mouseover', showTooltip)
        .on('mouseout', hideTooltip);
    
    // Add axes
    g.append('g')
        .attr('transform', `translate(0,${chartHeight})`)
        .call(d3.axisBottom(xScale))
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '.15em')
        .attr('transform', 'rotate(-45)');
    
    g.append('g')
        .call(d3.axisLeft(yScale));
    
    // Store visualization reference
    visualizations[containerId] = { svg, data };
}

// Utility Functions
function getNodeColor(type) {
    const colors = {
        'root': '#0d6efd',
        'pillar': '#198754',
        'category': '#ffc107',
        'sector': '#dc3545',
        'initiative': '#6f42c1',
        'action': '#20c997',
        'application': '#fd7e14'
    };
    return colors[type] || '#6c757d';
}

function showTooltip(event, d) {
    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip show')
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px');
    
    let content = `<strong>${d.name || d.country || d.theme}</strong>`;
    if (d.description) content += `<br>${d.description}`;
    if (d.budget) content += `<br>Budget: ${d.budget}`;
    if (d.value !== undefined) content += `<br>Value: ${d.value}`;
    
    tooltip.html(content);
}

function hideTooltip() {
    d3.selectAll('.tooltip').remove();
}

function showLoading() {
    const loadingHtml = `
        <div class="loading-spinner">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    
    document.querySelectorAll('.loading-target').forEach(element => {
        element.innerHTML = loadingHtml;
    });
}

function hideLoading() {
    document.querySelectorAll('.loading-spinner').forEach(element => {
        element.remove();
    });
}

function showError(message) {
    const alertHtml = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.getElementById('alert-container') || document.body;
    alertContainer.insertAdjacentHTML('afterbegin', alertHtml);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Search functionality
async function handleSearch(event) {
    const query = event.target.value.trim();
    if (query.length < 2) {
        clearSearchResults();
        return;
    }
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        displaySearchResults(data.results);
    } catch (error) {
        console.error('Search error:', error);
        showError('Search failed');
    }
}

function displaySearchResults(results) {
    const container = document.getElementById('search-results');
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No results found</p>';
        return;
    }
    
    const resultsHtml = results.map(result => `
        <div class="search-result-item">
            <h6><a href="/country/${result.country_code}">${result.country_name}</a></h6>
            <p class="text-muted mb-0">Relevance: ${result.relevance} matches</p>
        </div>
    `).join('');
    
    container.innerHTML = resultsHtml;
}

function clearSearchResults() {
    const container = document.getElementById('search-results');
    if (container) {
        container.innerHTML = '';
    }
}

// Comparison functionality
async function handleComparison() {
    const selectedCountries = getSelectedCountries();
    if (selectedCountries.length < 2) {
        showError('Please select at least 2 countries for comparison');
        return;
    }
    
    try {
        const params = selectedCountries.map(c => `countries=${c}`).join('&');
        const response = await fetch(`/api/comparison?${params}`);
        const data = await response.json();
        displayComparisonResults(data);
    } catch (error) {
        console.error('Comparison error:', error);
        showError('Comparison failed');
    }
}

function getSelectedCountries() {
    const checkboxes = document.querySelectorAll('input[name="countries"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function displayComparisonResults(data) {
    const container = document.getElementById('comparison-results');
    if (!container) return;
    
    // Implementation would depend on the specific comparison page layout
    console.log('Comparison results:', data);
}

// Export functionality
function handleExport() {
    const format = document.getElementById('export-format')?.value || 'json';
    const data = getCurrentPageData();
    
    if (format === 'json') {
        downloadJSON(data, 'ai-strategies-data.json');
    } else if (format === 'csv') {
        downloadCSV(data, 'ai-strategies-data.csv');
    }
}

function getCurrentPageData() {
    // Return current page data based on context
    return currentData;
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    downloadBlob(blob, filename);
}

function downloadCSV(data, filename) {
    // Convert data to CSV format
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    downloadBlob(blob, filename);
}

function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    // Simple CSV conversion - would need more sophisticated implementation
    if (!data || !Array.isArray(data)) return '';
    
    const headers = Object.keys(data[0] || {});
    const rows = data.map(row => 
        headers.map(header => `"${row[header] || ''}"`).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
}

// Resize handler for responsive visualizations
window.addEventListener('resize', debounce(function() {
    // Redraw visualizations on window resize
    Object.keys(visualizations).forEach(containerId => {
        const viz = visualizations[containerId];
        if (viz && viz.data) {
            // Redraw based on visualization type
            if (containerId.includes('mind-map')) {
                createMindMap(containerId, viz.data);
            } else if (containerId.includes('network')) {
                createNetworkGraph(containerId, viz.data);
            } else if (containerId.includes('timeline')) {
                createTimeline(containerId, viz.data);
            } else if (containerId.includes('heatmap')) {
                createHeatmap(containerId, viz.data);
            }
        }
    });
}, 250));

// Export functions for use in other scripts
window.AIStrategiesPortal = {
    createMindMap,
    createNetworkGraph,
    createTimeline,
    createHeatmap,
    showTooltip,
    hideTooltip,
    showLoading,
    hideLoading,
    showError
};
