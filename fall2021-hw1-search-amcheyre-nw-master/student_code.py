from expand import expand


def a_star_search (dis_map, time_map, start, end):

	closed_lst = []
	open_lst = []
	open_lst.append(start)

	# Cost to reach current_node n from start (use time map)
	g_funct = {}
	g_funct[start] = 0


	# Maping of nodes
	node_maping = {}
	node_maping[start] = start


	while len(open_lst) > 0:
		current_node = None

		# Find a node with the lowest value of f
		for v in open_lst:
			# h(n) = estimated cost from node to goal (use distance map)
			h_funct_v = dis_map[v][end]
			if current_node is not None:
				h_funct_n = dis_map[current_node][end]
				f_funct_n = g_funct[current_node] + h_funct_n
				f_funct_v = g_funct[v] + h_funct_v

			# Compare f(n) = estimated total cost of the route to the goal
			if current_node == None:
				current_node = v
			elif f_funct_n > f_funct_v:
				current_node = v
			elif f_funct_n == f_funct_v:
				# If tie, Check which of them has smallest h(n)
				if h_funct_n > h_funct_v:
					current_node = v
				elif h_funct_n < h_funct_v:
					current_node = n

		# When we finally find the end node
		if current_node == end:
			path = []

			while node_maping[current_node] is not current_node:
				path.append(current_node)
				current_node = node_maping[current_node]

			path.append(current_node)
			path.reverse()

			return path


		# For all the neighbors of the current node
		for neighbour in expand(current_node, time_map):
			t = time_map[current_node][neighbour]

			if neighbour not in open_lst and neighbour not in closed_lst:
				open_lst.append(neighbour)
				node_maping[neighbour] = current_node
				g_funct[neighbour] = g_funct[current_node] + t

			else:
				if g_funct[neighbour] > g_funct[current_node] + t:
					g_funct[neighbour] = g_funct[current_node] + t
					node_maping[neighbour] = current_node

					if neighbour in closed_lst:
						closed_lst.remove(neighbour)
						open_lst.append(neighbour)

		open_lst.remove(current_node)
		closed_lst.append(current_node)

	return None



def depth_first_search(time_map, start, end):
	current_node = start
	path = [current_node]
	fringe = []

	if current_node == end:
		return path

	neighbours = expand(current_node, time_map)
	neighbours.reverse()
	fringe.extend(neighbours)

	if fringe != None:
		for neighbour in fringe:
			dfs = depth_first_search(time_map, neighbour, end)

			if dfs is not None:

				if dfs[-1] == end:
					path.extend(dfs)
					return path

	else:
		return None

	return path



def breadth_first_search(time_map, start, end):

	shortest_paths = {start: (None, 0)}
	current_node = start
	visited = []

	while current_node is not end:
		visited.append(current_node)
		destinations = expand(current_node, time_map)
		time_to_current_node = shortest_paths[current_node][1]

		for next_node in destinations:
			total_time = time_map[current_node][next_node] + time_to_current_node
			if next_node not in shortest_paths:
				shortest_paths[next_node] = (current_node, total_time)
			else:
				current_shortest_total_time = shortest_paths[next_node][1]
				if current_shortest_total_time > total_time:
					shortest_paths[next_node] = (current_node, total_time)

		next_destinations = {}
		for n in shortest_paths:
			if n not in visited:
				next = { n : shortest_paths[n]}
				next_destinations.update(next)

		def other_dest(k):
			return next_destinations[k][1]

		current_node = min(next_destinations, key = other_dest)

	# Destinations in shortest path
	path = []
	while current_node is not None:
		path.append(current_node)
		next_node = shortest_paths[current_node][0]
		current_node = next_node

	path.reverse()
	return path
