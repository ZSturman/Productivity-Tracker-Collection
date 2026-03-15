//
//  NewTopicsView.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/28/23.
//


import SwiftUI
import CoreData

struct NewTopicView: View {
    var managedObjectContext: NSManagedObjectContext
    
    @FetchRequest(
        sortDescriptors: [NSSortDescriptor(keyPath: \TopicsEntity.name, ascending: true)],
        animation: .default)
    private var topics: FetchedResults<TopicsEntity>

    @State private var name: String = ""
    @State private var explanation: String = ""
    @State private var showingError = false
    @State private var errorMessage = ""

    var body: some View {
        NavigationView {
            VStack {
                List {
                    ForEach(topics) { topic in
                        NavigationLink(destination: TopicDetailView(topic: topic)) {
                            VStack(alignment: .leading) {
                                Text("Topic Name: \(topic.name ?? "")")
                                Text("Topic Explanation: \(topic.explanation ?? "")")
                            }
                        }
                    }
                }
                Form {
                    Section(header: Text("New Topic")) {
                        TextField("Topic Name", text: $name)
                        TextField("Topic Explanation", text: $explanation)
                        Button(action: {
                            addTopic()
                        }) {
                            Text("Add to topic list")
                        }
                    }
                }
            }
            .navigationTitle("Topics")
            .alert(isPresented: $showingError) {
                Alert(title: Text("Error"), message: Text(errorMessage), dismissButton: .default(Text("OK")))
            }
        }
    }

    private func addTopic() {
        guard !name.isEmpty else {
            errorMessage = "Name is required"
            showingError = true
            return
        }
        
        let newTopic = TopicsEntity(context: managedObjectContext)
        newTopic.id = UUID()
        newTopic.name = name
        newTopic.explanation = explanation

        do {
            try managedObjectContext.save()
            name = ""
            explanation = ""
        } catch {
            let nsError = error as NSError
            errorMessage = """
                            Error: \(nsError.localizedDescription)
                            """
            showingError = true
        }
    }
}

//struct NewTopicView_Previews: PreviewProvider {
//    static var previews: some View {
//        let dataController = DataController()
//        NewTopicView().environment(\.managedObjectContext, dataController.container.viewContext)
//    }
//}

struct TopicDetailView: View {
    var topic: TopicsEntity

    var body: some View {
        Text("Topic details for \(topic.name ?? "")")
    }
}
