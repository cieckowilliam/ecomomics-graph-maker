import matplotlib.pyplot as plt
from dataclasses import dataclass
from drafter import *

@dataclass
class Graph:
    title: str
    graph_type: str
    supply_slope: float
    demand_slope: float
    initial_supply: float
    initial_demand: float
    first_extra: float
    second_extra: float

@dataclass
class State:
    title: str
    graph_type: str
    supply_slope: float
    demand_slope: float
    initial_supply: float
    initial_demand: float
    first_extra: float
    second_extra: float
    saved_graphs: list[Graph]
    
GRAPH_TYPES = ["Supply and Demand", "Tariff", "Negative Externality"]

def draw_graph(state: State) -> None:
    plt.clf()
    demand_slope = state.demand_slope
    supply_slope = state.supply_slope

    initial_demand = state.initial_demand
    initial_supply = state.initial_supply
    
    if state.graph_type == "Supply and Demand":
        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply

        xs = [0, 2 * equilibrium_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MC", color = "blue" )
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, equilibrium_price, linestyles = "dashed", color = "black")
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black", label = "Equilibrium")
        
        plt.fill([0, equilibrium_quantity, 0],
                 [initial_demand, equilibrium_price, equilibrium_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, equilibrium_quantity, 0],
                 [initial_supply, equilibrium_price, equilibrium_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        
        plt.legend(loc = "upper center")
        plt.title("Market")
        plt.xlabel("Quantity")
        plt.ylabel("Price($)")
        plt.ylim(bottom = 0)
        plt.margins(0.025)
        
    elif state.graph_type == "Tariff":
        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply

        world_price = state.first_extra
        tariff_price = state.second_extra
        
        seller_trade_quantity = (world_price - initial_supply) / supply_slope
        seller_tariff_quantity = (tariff_price - initial_supply) / supply_slope
        buyer_tariff_quantity = (tariff_price - initial_demand) / demand_slope
        buyer_trade_quantity = (world_price - initial_demand) / demand_slope
        
        xs = [0, buyer_trade_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MC", color = "blue" )
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black", label = "Equilibrium")
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, equilibrium_price, linestyles = "dashed", color = "black")
        
        plt.hlines(tariff_price, 0, buyer_trade_quantity, linestyles = "dashed", color = "black")
        plt.hlines(world_price, 0, buyer_trade_quantity, linestyles = "dashed", color = "black")
        
        plt.vlines(seller_trade_quantity, 0, world_price, linestyles = "dashed", color = "black")
        plt.vlines(seller_tariff_quantity, 0, tariff_price, linestyles = "dashed", color = "black")
        plt.vlines(buyer_tariff_quantity, 0, tariff_price, linestyles = "dashed", color = "black")
        plt.vlines(buyer_trade_quantity, 0, world_price, linestyles = "dashed", color = "black")
        
        plt.fill([0, buyer_tariff_quantity, 0],
                 [initial_demand, tariff_price, tariff_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, seller_tariff_quantity, 0],
                 [initial_supply, tariff_price, tariff_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        plt.fill([seller_tariff_quantity, buyer_tariff_quantity, buyer_tariff_quantity, seller_tariff_quantity],
                 [world_price, world_price, tariff_price, tariff_price],
                 color = "lightgreen",
                 label = "Government Revenue")
        plt.fill([buyer_trade_quantity, buyer_tariff_quantity, buyer_tariff_quantity],
                 [world_price, world_price, tariff_price],
                 color = "khaki")
        plt.fill([seller_trade_quantity, seller_tariff_quantity, seller_tariff_quantity],
                 [world_price, world_price, tariff_price],
                 color = "khaki",
                 label = "Dead Weight Loss")
        
        plt.legend(loc = "upper right")
        plt.title("Market")
        plt.xlabel("Quantity")
        plt.ylabel("Price($)")
        plt.ylim(bottom = 0)
        plt.ylim(top = initial_demand)

    elif state.graph_type == "Negative Externality":
        externality_slope = state.first_extra
        initial_externality = state.second_extra

        equilibrium_quantity = (initial_supply - initial_demand) / (demand_slope - supply_slope)
        equilibrium_price = supply_slope * equilibrium_quantity + initial_supply
        
        socially_optimal_quantity = (initial_externality - initial_demand) / (demand_slope - externality_slope)
        socially_optimal_price = externality_slope * socially_optimal_quantity + initial_externality
        peak_social_cost = externality_slope * equilibrium_quantity + initial_externality

        xs = [0, 2 * equilibrium_quantity]

        dy = [demand_slope * x + initial_demand for x in xs]
        sy = [supply_slope * x + initial_supply for x in xs]
        ey = [externality_slope * x + initial_externality for x in xs]

        plt.plot(xs, dy, label = "Demand = MB", color = "red")
        plt.plot(xs, sy,label = "Supply = MPC", color = "blue" )
        plt.plot(xs, ey,label = "MSC", color = "black" )
        
        plt.hlines(equilibrium_price, 0, equilibrium_quantity, linestyles = "dashed", color = "black")
        plt.vlines(equilibrium_quantity, 0, peak_social_cost, linestyles = "dashed", color = "black")
        plt.scatter(equilibrium_quantity, equilibrium_price, zorder = 10, color = "black")
        
        plt.hlines(socially_optimal_price, 0, socially_optimal_quantity, linestyles = "dashed", color = "black")
        plt.vlines(socially_optimal_quantity, 0, socially_optimal_price, linestyles = "dashed", color = "black")
        plt.scatter(socially_optimal_quantity, socially_optimal_price, zorder = 10, color = "black")

        plt.fill([0, 0, equilibrium_quantity],
                 [initial_demand, equilibrium_price, equilibrium_price],
                 color = "lightcoral",
                 label = "Consumer Surplus")
        plt.fill([0, 0, equilibrium_quantity],
                 [initial_supply, equilibrium_price, equilibrium_price],
                 color = "skyblue",
                 label = "Producer Surplus")
        plt.fill([socially_optimal_quantity, equilibrium_quantity, equilibrium_quantity],
                 [socially_optimal_price, equilibrium_price, peak_social_cost],
                 color = "khaki",
                 label = "Dead Weight Loss")
            
        plt.legend(loc = "upper center")
        plt.title("Market")
        plt.xlabel("Quantity")
        plt.ylabel("Price($)")
        plt.ylim(bottom = 0)

@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Microeconomic Graph Maker", 1),
        Button("Start", select_graph)
        ])

@route
def select_graph(state: State) -> Page:
    return Page(state, [
        Header("Select Graph Type", 2),
        "Graph Type:",
        SelectBox("graph_type", GRAPH_TYPES, state.graph_type),
        Button("Next", save_type)
        ])

@route
def save_type(state: State, graph_type: str) -> Page:
    state.graph_type = graph_type
    return(enter_inputs(state))

@route
def enter_inputs(state: State) -> Page:
    input_fields = [
        Header("Input Graph Information", 2),
        "Title:", TextBox("title", state.title),
        "Supply Slope:", TextBox("supply_slope", state.supply_slope),
        "Demand Slope:", TextBox("demand_slope", state.demand_slope),
        "Initial Supply:", TextBox("initial_supply", state.initial_supply),
        "Initial Demand:", TextBox("initial_demand", state.initial_demand),
        ]
    
    if state.graph_type == "Tariff":
        input_fields += ["World Price", TextBox("first_extra", state.first_extra),
                         "Tariff Price", TextBox("second_extra", state.second_extra)]
        return Page(state, input_fields + [Button("Make Graph", save_extra_inputs)])
    
    if state.graph_type == "Negative Externality":
        input_fields += ["MSC Slope", TextBox("first_extra", state.first_extra),
                         "MSC Intercept", TextBox("second_extra", state.second_extra)]
        return Page(state, input_fields + [Button("Make Graph", save_extra_inputs)])
    return Page(state, input_fields + [Button("Make Graph", save_inputs)])
    
@route
def save_inputs(state: State, title: str,
                supply_slope: float, demand_slope: float, initial_supply: float, initial_demand: float) -> Page:
    state.title = title
    state.supply_slope = supply_slope
    state.demand_slope = demand_slope
    state.initial_supply = initial_supply
    state.initial_demand = initial_demand
    return show_graph(state)

@route
def save_extra_inputs(state: State, title: str,
                      supply_slope: float, demand_slope: float, initial_supply: float, initial_demand: float,
                      first_extra: float, second_extra: float) -> Page:
    state.title = title
    state.supply_slope = supply_slope
    state.demand_slope = demand_slope
    state.initial_supply = initial_supply
    state.initial_demand = initial_demand
    state.first_extra = first_extra
    state.second_extra = second_extra
    return show_graph(state)

    
@route
def show_graph(state: State) -> Page:
    draw_graph(state)
    return Page(state, [
        Header(state.title, 2),
        MatPlotLibPlot(),
        Button("Save Graph", save_graph),
        Button("Saved Graphs", view_saved_graphs)
        ])

@route
def save_graph(state: State) -> Page:
    new_graph = Graph(state.title, state.graph_type,
                      state.supply_slope, state.demand_slope, state.initial_supply, state.initial_demand,
                      state.first_extra, state.second_extra)
    state.saved_graphs.append(new_graph)
    return view_saved_graphs(state)

@route
def view_saved_graphs(state: State) -> Page:
    if len(state.saved_graphs) == 0:
        return Page(state, [
            Header("Saved Graphs", 2),
            "No Saved Graphs",
            Button("Home", index)])
    
    titles = []
    for graph in state.saved_graphs:
        titles.append(graph.title)
        
    return Page(state, [
        Header("Saved Graphs", 2),
        SelectBox("choice", titles, titles[0]),
        Button("Open", open_saved_graphs),
        Button("Home", index)])
    
@route
def open_saved_graphs(state: State, choice: str) -> Page:
    for graph in state.saved_graphs:
        if graph.title == choice:
            state.title = graph.title
            state.graph_type = graph.graph_type
            state.supply_slope = graph.supply_slope
            state.demand_slope = graph.demand_slope
            state.initial_supply = graph.initial_supply
            state.initial_demand = graph.initial_demand
            state.first_extra = graph.first_extra
            state.second_extra = graph.second_extra
    return show_graph(state)

start_server(State("My Graph", "Supply and Demand", 1.0, -1.0, 2.0, 20.0, 0.0, 0.0, []))
