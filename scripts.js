document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for navigation links
    document.querySelectorAll('.nav-links a, .nav-brand a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        });
    });

    // Navigation buttons
    document.querySelectorAll('.nav-button').forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.dataset.section;
            const section = document.getElementById(sectionId);
            section.scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Intersection Observer for section animations
    const sections = document.querySelectorAll('.section');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px'
    };

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                sectionObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    sections.forEach(section => {
        section.style.opacity = '0';
        sectionObserver.observe(section);
    });

    // Example: Navigation toggle for small screens
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('show');
        });
    }

    // Nuclear energy visualization
    fetch('summed_nuclear_data.json')
        .then(response => response.json())
        .then(data => {
            // Extract data for plotting
            const countryNames = data.map(item => item['Country/Area']);
            const capacities = data.map(item => item['Capacity (MW)']);
            const hoverText = data.map(item =>
                `${item['Country/Area']}<br>Capacity: ${item['Capacity (MW)'].toLocaleString()} MW`
            );

            // Define the Plotly trace
            const trace = {
                type: 'choropleth',
                locations: countryNames,
                locationmode: 'country names',
                z: capacities,
                text: hoverText,
                colorscale: [
                    [0, 'rgb(255, 255, 204)'],
                    [0.25, 'rgb(255, 237, 160)'],
                    [0.5, 'rgb(254, 178, 76)'],
                    [0.75, 'rgb(240, 59, 32)'],
                    [1, 'rgb(189, 0, 38)']
                ],
                autocolorscale: false,
                reversescale: false,
                zmin: Math.min(...capacities),
                zmax: Math.max(...capacities),
                marker: {
                    line: {
                        color: 'rgb(180,180,180)',
                        width: 0.5
                    }
                },
                colorbar: {
                    title: 'Capacity (MW)',  
                    thickness: 15
                }
            };

            // Define the layout
            const layout = {
                geo: {
                    projection: {
                        type: 'orthographic',
                        rotation: { lon: 0, lat: 1, roll: 0 },
                        scale: 1
                    },
                    showland: true,
                    landcolor: 'rgb(240,240,240)',
                    countrycolor: 'rgba(200, 200, 200, 0.5)',
                    bgcolor: 'rgba(0,0,0,0)',
                    showocean: true,
                    oceancolor: 'rgb(0, 40, 160)',
                    lakecolor: 'rgb(158, 193, 320)',
                    resolution: 1000
                },
                paper_bgcolor: 'rgba(0,0,0,0)',
                margin: { l: 0, r: 0, t: 50, b: 0 },
                height: 550
            };

            // Render the map
            Plotly.newPlot('map-container', [trace], layout, { 
                responsive: true,
                displayModeBar: false
            })
            .then(() => {
                let longitude = 0;
                let isInteracting = false;
                let isRotating = true;
                let is3D = true;

                // Create controls container
                const mapContainer = document.getElementById('map-container');
                const controlsContainer = document.createElement('div');
                controlsContainer.className = 'map-controls';
                mapContainer.appendChild(controlsContainer);

                // Add rotation control button
                const rotationButton = document.createElement('button');
                rotationButton.className = 'map-control-button';
                rotationButton.textContent = 'Stop Rotation';
                controlsContainer.appendChild(rotationButton);

                // Add projection toggle button
                const projectionButton = document.createElement('button');
                projectionButton.className = 'map-control-button';
                projectionButton.textContent = 'Switch to 2D';
                controlsContainer.appendChild(projectionButton);

                // Rotation control click handler
                rotationButton.addEventListener('click', () => {
                    isRotating = !isRotating;
                    rotationButton.textContent = isRotating ? 'Stop Rotation' : 'Start Rotation';
                });

                // Projection toggle click handler
                projectionButton.addEventListener('click', () => {
                    is3D = !is3D;
                    projectionButton.textContent = is3D ? 'Switch to 2D' : 'Switch to 3D';
                    
                    if (is3D) {
                        // Reset to initial 3D state
                        longitude = 0;
                        isRotating = true;
                        rotationButton.textContent = 'Stop Rotation';
                        rotationButton.disabled = false;
                        
                        const initialLayout = {
                            geo: {
                                projection: {
                                    type: 'orthographic',
                                    rotation: { lon: 0, lat: 1, roll: 0 },
                                    scale: 1
                                },
                                showland: true,
                                landcolor: 'rgb(240,240,240)',
                                countrycolor: 'rgba(200, 200, 200, 0.5)',
                                bgcolor: 'rgba(0,0,0,0)',
                                showocean: true,
                                oceancolor: 'rgb(0, 40, 160)',
                                lakecolor: 'rgb(158, 193, 320)',
                                resolution: 1000,
                                showframe: false
                            }
                        };
                        
                        Plotly.relayout('map-container', initialLayout);
                    } else {
                        // Switch to 2D
                        const newLayout = {
                            'geo.projection': {
                                type: 'equirectangular',
                                scale: undefined
                            },
                            'geo.center': { lon: 0, lat: 0 },
                            'geo.showframe': true,
                            'geo.showcountries': true,
                            'geo.showcoastlines': true,
                            'geo.showland': true,
                            'geo.showocean': true,
                            'geo.oceancolor': 'rgb(0, 40, 160)',
                            'geo.landcolor': 'rgb(240,240,240)',
                            'geo.countrycolor': 'rgba(200, 200, 200, 0.5)',
                            'geo.framecolor': 'rgba(200, 200, 200, 0.5)',
                            'geo.framewidth': 1
                        };

                        Plotly.relayout('map-container', newLayout);
                        isRotating = false;
                        rotationButton.textContent = 'Start Rotation';
                        rotationButton.disabled = true;
                    }
                });

                function rotate() {
                    if (!isInteracting && isRotating && is3D) {
                        longitude = (longitude + 0.5) % 360;
                        Plotly.relayout('map-container', {
                            'geo.projection.rotation.lon': longitude
                        });
                    }
                    requestAnimationFrame(rotate);
                }

                // Start rotation
                rotate();

                // Mouse interaction events
                mapContainer.addEventListener('mouseenter', () => {
                    isInteracting = true;
                });

                mapContainer.addEventListener('mouseleave', () => {
                    isInteracting = false;
                });

                // Handle dragging
                mapContainer.addEventListener('mousedown', () => {
                    isInteracting = true;
                });

                document.addEventListener('mouseup', () => {
                    isInteracting = false;
                });
            });
        })
        .catch(error => console.error('Error loading JSON:', error));
});