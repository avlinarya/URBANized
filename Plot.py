def plot_city_layoutout(zone_coords):
    import matplotlib.pyplot as plt
    import numpy as np

    import plotly.graph_objects as go

    zone_styles = {
        'residential': {'color': 'brown', 'label': 'Residential'},
        'greenery': {'color': 'green', 'label': 'Walkable Greenery'},
        'transit': {'color': 'yellow', 'label': 'Transit Stop'},
        'school': {'color': 'purple', 'label': 'School'},
        'hospital': {'color': 'red', 'label': 'Hospital'},
        'water': {'color': 'blue', 'label': 'Water Body'},
        'roads': {'color': 'gray', 'label': 'Road'},
        'police_station': {'color': 'black', 'label': 'Police Station'},
        'fire_station': {'color': 'orange', 'label': 'Fire Station'},
        'commercial': {'color': 'pink', 'label': 'Commercial'},
    }


    def plot_city_layout(zone_styles, zone_coords, grid_size=10):
        fig = go.Figure()

        
        for zone_type, rects in zone_coords.items():
            style = zone_styles[zone_type]
            for x0, y0, x1, y1 in rects:
                fig.add_shape(
                    type="rect",
                    x0=x0, y0=y0,
                    x1=x1, y1=y1,
                    fillcolor=style["color"],
                    line=dict(color="black")
                    )


        
        for zone_type, style in zone_styles.items():
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color=style['color']),
                legendgroup=zone_type,
                showlegend=True,
                name=style['label']
            ))

        
        fig.update_layout(
        xaxis=dict(
            range=[0, 2000],
            showticklabels=False, 
            showgrid=False,
            zeroline=False,
            tickmode='linear',
            tick0=0,
            dtick=0
        ),
        yaxis=dict(
            range=[2000, 0],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            tickmode='linear',
            tick0=0,
            dtick=0
        ),
        title=" City Plan Layout ",
        width=900,
        height=700,
        plot_bgcolor="beige",
        margin=dict(l=20, r=120, t=40, b=20),
        xaxis_scaleanchor="y"    
        
    )


        return fig


    fig = plot_city_layout(zone_styles, zone_coords)
    fig.show()



