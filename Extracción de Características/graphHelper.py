def arts(graph):
    result = []
    visited, stack = set(), list(graph.keys())
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack2 = [x for x in graph[vertex] if x not in visited]
            stack.extend(stack2)
            while stack2:
                vertex2 = stack2.pop()
                nodes = [x for x in graph[vertex2] if x not in visited]
                for vertex3 in nodes:
                    result.append([vertex, vertex2, vertex3])
    return result
