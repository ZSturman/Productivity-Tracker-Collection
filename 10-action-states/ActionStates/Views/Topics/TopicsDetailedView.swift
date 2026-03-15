//
//  TopicsDetailedView.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/25/23.
//

import SwiftUI

struct TopicsDetailedView: View {
    let topic: TopicEntity
    
    @Environment(\.managedObjectContext) var moc
    @Environment(\.dismiss) var dismiss
    @State private var showingDeleteAlert = false
    
    var body: some View {
        ScrollView {
            Text(topic.topicDescription ?? "")
                .padding()
            
            ForEach(Array(topic.actionStates as? Set<ActionStateEntity> ?? []), id: \.self) { actionState in
                Text(actionState.name ?? "")
                    .padding()
            }
            
        }
        .navigationTitle(topic.name ?? "")
        .alert("Delete Topic?", isPresented: $showingDeleteAlert) {
            Button("Delete", role: .destructive, action: deleteTopic)
            Button("Cancel", role: .cancel) {}
        } message: {
            Text("Are you sure?")
        }
        .toolbar {
            Button {
                showingDeleteAlert = true
            } label : {
                Label("Delete Topic", systemImage: "trash")
            }
        }
    }
    
    func deleteTopic() {
        moc.delete(topic)
        
        //try? moc.save()
        dismiss()
    }
}
