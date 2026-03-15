//
//  TopicsListView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//

import CoreData
import SwiftUI

struct TopicsListView: View {
    @Environment(\.managedObjectContext) var moc
    @FetchRequest(sortDescriptors: [
        SortDescriptor(\.name)
    ]) var topics: FetchedResults<TopicEntity>
    
    @StateObject var topicViewModel: TopicViewModel
    
    @State private var showAddTopicScreen = false
    
    var body: some View {
        VStack() {
            List {
                ForEach(topics, id: \.id) { topic in
                    NavigationLink {
                        TopicsDetailedView(topic: topic)
                    } label: {
                        Text(topic.name ?? "No Title")
                            .font(.headline)
                    }
                }
                .onDelete(perform: topicViewModel.deleteTopic)
            }
        
        }
        .navigationTitle("Topics")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button {
                    showAddTopicScreen.toggle()
                } label: {
                    Label("Add Topic", systemImage: "plus")
                }
            }
        }
        .sheet(isPresented: $showAddTopicScreen) {
            AddTopicView(moc: self.moc)
                .environment(\.managedObjectContext, self.moc)
        }
    }
    

}
