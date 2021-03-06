#!/usr/bin/env python3
"""
This script loads a robot.yaml file and inserts it into the simulator.
"""

import os
import sys
import asyncio
from pyrevolve.SDF.math import Vector3
from pyrevolve import revolve_bot, parser
from pyrevolve.tol.manage import World
from pyrevolve.util.supervisor.supervisor_multi import DynamicSimSupervisor
from pyrevolve.evolution import fitness
import numpy as np


async def run():

    arguments = parser.parse_args()
    working_path = "experiments/bodies/"
    robot_file_path = []
    if arguments.robot_name is not None:
        for f in os.listdir(working_path):
            if f.startswith(arguments.robot_name):
                robot_file_path.append(f)

    # Parse command line / file input arguments
    settings = parser.parse_args()

    print("Starting Args:", settings)

    # Start Simulator
    if settings.simulator_cmd != 'debug':
        simulator_supervisor = DynamicSimSupervisor(
            world_file=settings.world,
            simulator_cmd=settings.simulator_cmd,
            simulator_args=["--verbose"],
            plugins_dir_path=os.path.join('.', 'build', 'lib'),
            models_dir_path=os.path.join('.', 'models'),
            simulator_name='gazebo'
        )
        await simulator_supervisor.launch_simulator(port=settings.port_start)
        await asyncio.sleep(0.1)

    # Connect to the simulator and pause
    connection = await World.create(settings, world_address=('127.0.0.1', settings.port_start))
    await asyncio.sleep(1)

    # Starts the simulation
    await connection.pause(False)

    # Load a robot from yaml
    robot = []
    for i in range(len(robot_file_path)):
        r = revolve_bot.RevolveBot()
        r.load_file(os.path.join(working_path,robot_file_path[i]))
        r.update_substrate()
        #await asyncio.sleep(0.1)
        robot.append(r)
        robot[len(robot)-1].update_substrate()
    #    robot_manager = await connection.insert_robot(
    #        robot[i], Vector3(0, 5*i, settings.z_start))
    managers = []
    xy = np.mgrid[-35:35:10, -35:35:10].reshape(2, -1).T #49 robots possible
    for i, r in enumerate(robot):
         managers.append(await connection.insert_robot(
                     r, Vector3(xy[i, 0], xy[i, 1], settings.z_start)))#, life_timeout=60))

    status = 'dead' if managers[-1].dead else 'alive'

    while status is 'alive':
        status = 'dead' if managers[-1].dead else 'alive'
        print(f"Robot is {status}")
        await asyncio.sleep(1)

    fitnesses=[] #Hobbitses :)
    fitnesses_hill = []
    for i in range(len(robot)):
        fitnesses.append(fitness.displacement_velocity(managers[i], robot[i]))
        fitnesses_hill.append(fitness.displacement_velocity_hill(managers[i], robot[i]))
    out_data = [fitnesses, fitnesses_hill]

    print(f"**The Data is: {out_data} \n")