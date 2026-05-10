# Real-Time Seismic Activity Monitoring Web Application

## Live Demo

https://earthquakes-monitoring-webapp.vercel.app

## Overview

This is a full-stack web application for monitoring and visualizing earthquake activity in Greece.

It provides:

- Historical earthquake data imported from an Excel file.
- Latest earthquake updates from the University of Athens seismicity XML feed.
- Interactive Leaflet map with clustered markers and heatmap visualization.
- Dynamic statistics sidebar with charts for earthquake count, average magnitude, and maximum magnitude over time.
- Advanced filtering by date, latitude, longitude, depth, and magnitude.
- A protected backend update endpoint for scheduled data refreshes.

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** React, Vite, Leaflet, Recharts
- **Local Database:** SQLite
- **Production Database:** PostgreSQL, for example Neon
- **Backend Deployment:** Render
- **Frontend Deployment:** Vercel
- **Scheduled Updates:** cron-job.org or another external scheduler
- **Data Source:** XML feed from the Department of Geology and Geoenvironment, National and Kapodistrian University of Athens

---

## Features

- Earthquake list with table view and filters.
- Interactive Leaflet map with markers and clustering.
- Heatmap layer for large datasets.
- Dynamic statistics charts using Recharts.
- Historical earthquake import from Excel.
- Latest earthquake fetching from XML feed.
- Protected update endpoint for scheduled production refreshes.
- Deployment-ready configuration using environment variables.

![Project Screenshot](assets/dashboard.png)

![Statistics Sidebar](assets/stats_sidebar.png)

---

## Abstract

This project is part of my Master’s thesis in Control and Computing at the National and Kapodistrian University of Athens. It presents an integrated web application for real-time monitoring and visualization of seismic activity in Greece.

The main objective is the automated collection, processing, and visualization of earthquake data. The application combines backend and frontend technologies to deliver a complete system that allows dynamic user interaction with geospatial data through a modern, user-friendly web interface.

Seismic data are retrieved in XML format from the public website of the Department of Geology and Geoenvironment of the National and Kapodistrian University of Athens. These data are processed and stored in the application’s database, while a REST API built with Django REST Framework exposes them to the frontend for interactive visualization.

The frontend, developed with React, Vite, and Leaflet, provides a rich map interface where users can view recent earthquakes or filter data by date range, coordinates, depth, and magnitude. Additional visualization options, such as clustering and heatmaps, enhance understanding of seismic trends over time.

Overall, this application offers an accessible platform for both researchers and the public to explore historical and near-real-time seismic activity in Greece. It also serves as a foundation for future extensions, such as notifications, predictive modeling, and integration with international seismic data networks.

---
