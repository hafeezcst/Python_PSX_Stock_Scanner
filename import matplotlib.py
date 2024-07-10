import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import altair as alt

# Customizable Parameters
amplitude = 1.0
wavelength = 5.0
frequency = 1.0
arrow_density = 20  # Number of arrows per unit length
arrow_color = 'blue'
wave_color = 'lightgray'
x_start, x_end = -10, 10
y_start, y_end = -1.2, 1.2
frames = 100
interval = 20  # Delay between frames (ms)

# Calculated Values
phase_velocity = wavelength * frequency
x = np.linspace(x_start, x_end, int((x_end - x_start) * arrow_density))
t_start, t_end = 0, wavelength / phase_velocity  # One full cycle

# Calculate initial y_wave for the chart
y_wave_initial = amplitude * np.sin(2 * np.pi * (x / wavelength - frequency * t_start))

# Create a chart to visualize the wave (static plot)
data = pd.DataFrame({'x': x, 'y': y_wave_initial})
chart = alt.Chart(data).mark_line().encode(
    x='x',
    y='y'
).properties(
    title='Traveling Wave (Initial State)'
).interactive()

chart.save('traveling_wave_visualization.json')


# Figure Setup
fig, ax = plt.subplots()
ax.set_xlim([x_start, x_end])
ax.set_ylim([y_start, y_end])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Traveling Wave Animation (Vertical Arrows)')

# Shift spines to the center
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


# Initialize ONLY vertical arrows
arrows_vertical = []
for xi in x:
    arrow = ax.arrow(xi, 0, 0, 0, head_width=0.2, head_length=0.3, fc=arrow_color, ec=arrow_color)
    arrows_vertical.append(arrow)


# Animation function (modified)
def animate(frame):
    t = t_start + (t_end - t_start) * frame / frames
    y_wave = amplitude * np.sin(2 * np.pi * (x / wavelength - frequency * t))

    # Plot the vertical wave
    ax.plot(x, y_wave, color=wave_color, alpha=0.5)

    for i in range(len(x)):
        arrows_vertical[i].set_data(x=x[i], y=0, dx=0, dy=y_wave[i])
    return arrows_vertical  # Return only vertical arrows


# Create the animation
animation = FuncAnimation(fig, animate, frames=frames, interval=interval, blit=True, repeat=True)

# Add this line to prevent the '_resize_id' error:
animation._resize_id = fig.canvas.mpl_connect('resize_event', animation._handle_resize)

plt.show()
